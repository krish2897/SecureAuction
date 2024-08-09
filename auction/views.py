import asyncio
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.utils import timezone
from django.db.models import Q

from .models import CustomUser, Auction, BidsToAuction
from .forms import UserSignupForm, UserLoginForm, AddAuctionForm, ApplyToAuctionForm
from .nillion.libs import store_program_nillion, store_secret_nillion

def home_view(request):
    template = loader.get_template('home.html')

    return HttpResponse(template.render(request=request))

def auction_view(request):
    template = loader.get_template('auctions.html')

    return HttpResponse(template.render(request=request))

def user_signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            if user.is_auctioner:
                return redirect('auctioner')
            else:
                return redirect('bidder')
    else:
        form = UserSignupForm()
    template = loader.get_template('signup_page.html')

    return HttpResponse(template.render({'form': form}, request=request))


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                if user.is_auctioner:
                    return redirect('auctioner')
                else:
                    return redirect('bidder')
    else:
        form = UserLoginForm()
    template = loader.get_template('login_page.html')
    return HttpResponse(template.render({'form': form}, request=request))


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def auctioner_view(request):
    if request.user.is_auctioner:
        template = loader.get_template('auctioner_page.html')

        filter_type = request.GET.get('filter')
        search_query = request.GET.get('search')
        auctions_created = Auction.objects.filter(auctioner=request.user)

        if filter_type == 'completed':
            auctions_created = auctions_created.filter(ending_date__lt=timezone.now())
        elif filter_type == 'ongoing':
            auctions_created = auctions_created.filter(ending_date__gt=timezone.now(), created_date__lt=timezone.now(), is_closed=False)
        elif filter_type == 'upcoming':
            auctions_created = auctions_created.filter(created_date__gt=timezone.now())

        if search_query:
            auctions_created = auctions_created.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query)
            )

        context = {
            "auction_list": auctions_created,
            "search_query": search_query,
            "filter_type": filter_type,
        }

        return HttpResponse(template.render(context=context, request=request))
    
    return redirect('login')


@login_required
def add_auction_view(request):
    if request.user.is_auctioner:
        if request.method == 'POST':
            form = AddAuctionForm(request.POST, request.FILES)
            if form.is_valid():
                auction = form.save(commit=False)
                auction.auctioner = request.user
                program_id = asyncio.run(store_program_nillion.store_program_in_nillion())
                auction.program_id = program_id
                auction.save()

                return redirect('auctioner')

            else:
                print(form.errors)
        else:
            form = AddAuctionForm()
        template = loader.get_template('add_auction_page.html')
        return HttpResponse(template.render(context={'form':form}, request=request))
    
    return redirect('login')


@login_required
def bidder_view(request):
    if not request.user.is_auctioner:
        template = loader.get_template("bidder_page.html")

        search_query = request.GET.get('search')
        filter_query = request.GET.get('filter')
        view_applied = request.GET.get('view') == 'applied'

        applied_bids = BidsToAuction.objects.select_related('auction').filter(bidder=request.user)
        applied_list = []
        for bid in applied_bids:
            applied_list.append({
                'id': bid.auction.pk,
                'name': bid.auction.name,
                'base_price': bid.auction.base_price,
                'description': bid.auction.description,
                'image': bid.auction.image,
                'ending_date': bid.auction.ending_date,
                'is_closed': bid.auction.is_closed,
                'bid_count': bid.auction.bid_count,
                'max_bids': bid.auction.max_bids,
                'winner': bid.auction.get_winner(),
                'bidding_date': bid.bidding_date,
                'auctioner': bid.auction.auctioner
            })

        available_list = Auction.objects.filter(is_closed=False).exclude(bidstoauction__bidder=request.user)

        if search_query:
            available_list = available_list.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
            applied_list = [auction for auction in applied_list if search_query.lower() in auction['name'].lower() or search_query.lower() in auction['description'].lower()]

        if filter_query == 'completed':
            available_list = available_list.filter(ending_date__lt=timezone.now())
            applied_list = [auction for auction in applied_list if auction['is_closed']]
        elif filter_query == 'ongoing':
            available_list = available_list.filter(ending_date__gt=timezone.now(), created_date__lt=timezone.now(), is_closed=False)
            applied_list = [auction for auction in applied_list if not auction['is_closed']]
        elif filter_query == 'upcoming':
            available_list = available_list.filter(ending_date__gt=timezone.now())
            applied_list = [auction for auction in applied_list if auction['ending_date'] > timezone.now()]

        context = {
            'applied_list': applied_list,
            'available_list': available_list,
            'search_query': search_query,
            'filter_query': filter_query,
            'view_applied': view_applied,
        }

        return HttpResponse(template.render(context=context, request=request))
    
    return redirect('login')


@login_required
def auction_detail_view(request, id):
    # if not request.user.is_auctioner:
    auction = get_object_or_404(Auction, pk=id)
    if request.method == 'POST':
        form = ApplyToAuctionForm(data=request.POST)
        if form.is_valid():
            amount = form.cleaned_data.get('amount')
            
            if amount < auction.base_price:
                return HttpResponse("Amount cannot be less than base price")

            if auction.bid_count() < 10:
                bid_no = auction.bid_count() + 1

                store_id = asyncio.run(store_secret_nillion.store_secret_in_nillion(auction.program_id, amount, bid_no))

                bid_obj = BidsToAuction(auction=auction, bidder=request.user, store_id=store_id, bid_number=bid_no)
                bid_obj.save()
                return redirect('bidder')
            else:
                return HttpResponse("Already 10 bids in the auction")
        else:
            print(form.errors)
    else:
        can_bidder_apply = True
        if not request.user.is_auctioner:
            if BidsToAuction.objects.filter(auction=auction, bidder=request.user).exists():
                can_bidder_apply = False
        form = ApplyToAuctionForm()
        context = {
            'auction': auction,
            'form': form,
            'can_bidder_apply': can_bidder_apply
        }
        template = loader.get_template('auction_detail_page.html')

        return HttpResponse(template.render(context=context, request=request))
        
    # return redirect('login')


