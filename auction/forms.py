from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import CustomUser, Auction, BidsToAuction


class UserSignupForm(UserCreationForm):
    USER_TYPE_CHOICES = (
        ('auctioner', 'Auctioner'),
        ('bidder', 'Bidder')
    )

    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True)
    class Meta:
        model = CustomUser
        fields = ['username','user_type', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user_type = self.cleaned_data['user_type']

        user.is_auctioner = False
        if user_type == 'auctioner':
            user.is_auctioner = True

        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class AddAuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['name', 'description', 'image', 'base_price']
        

class ApplyToAuctionForm(forms.Form):
    amount = forms.IntegerField(required=True)
