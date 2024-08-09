## SecureAuction

SecureAuction is a robust web application designed for online auctions with enhanced security features. Bidders can confidently place bids on auctions, while auctioneers can seamlessly list items for bidding. SecureAuction harnesses the power of the Nillion network to provide a highly secure bidding environment, safeguarding users from data breaches and ensuring a trustworthy auction process.

## Features

- **Secure Bidding:** Leverages the Nillion Network to ensure secure and private bid placements.
- **Auction Posting:** Streamlined process for auctioneers to list and manage items for auction.
- **User-Friendly Interface:** Designed with simplicity and ease of use in mind for both bidders and auctioneers.
- **Item Search:** Quickly find and bid on specific items of interest.
- **Real-Time Updates:** Stay informed with live updates on auction status and bid activity.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [For Bidders](#for-bidders)
  - [For Auctioneers](#for-auctioneers)
- [Demo](#demo)
- [Security](#security)
- [Contributing](#contributing)
- [License](#license)

## Installation
You need to have [nillion-sdk](https://docs.nillion.com/nillion-sdk-and-tools) installed. Follow through the given link to install it.

Now create a virtual environment, activate it and install the requirements.
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Now you need to start the local nillion network.
```bash
cd auction/nillion
./bootstrap-local-environment.sh
cd ../..
```

Run migrate command.
```bash
python3 manage.py migrate
```
You need to have `redis-server` installed in you machine. You can install it with:
```bash
sudo apt install redis-server
```
Then start it with:
```bash
sudo systemctl start redis-server
```
Now we can run the application. Run following 4 commands in seperate terminal.
```bash
python manage.py runserver
python manage.py tailwind start
celery -A bidding beat --loglevel=info
celery -A bidding worker --loglevel=info
```
### Prerequisites

- Python


## Usage

### For Bidders

1. **Register/Login:**
   - Create an account or log in with your existing credentials.

2. **Browse Auctions:**
   - View a list of available auctions and detailed information about each item.

3. **Place a Bid:**
   - Select an auction and enter your bid amount.
   - Bids are securely processed using Nillion Network.

4. **Monitor Auctions:**
   - Track your bids and get real-time updates on auction status.

### For Auctioneers

1. **Register/Login:**
   - Create an account or log in with your existing credentials.

2. **Post an Auction:**
   - Click on "Add Auction" and fill out the item details, including title, description, and starting bid.

3. **Manage Auctions:**
   - View your posted auctions.
   - Monitor bids and auction progress.

## Demo


https://github.com/Sandesh-Pyakurel/Bidding/assets/82999440/019af915-c659-41ab-a2c0-c3f39da5ee07



## Security

BidSecure prioritizes the security and privacy of user data. We use Nillion Network to ensure that all bids are encrypted and securely processed, preventing data leakage and unauthorized access. For more details, visit the [Nillion website](https://www.nillion.com).

## Contributing

We welcome contributions to BidSecure! Please follow these steps to contribute:

1. **Fork the Repository**: Click the "Fork" button on GitHub to create your copy.

2. **Clone Your Fork**:
   ```bash
   git clone https://github.com/Sandesh-Pyakurel/Bidding.git
   ```

3. **Create a Branch**:
   ```bash
   git checkout -b your-branch-name
   ```

4. **Make Changes**: Implement your changes.

5. **Commit Your Changes**:
   ```bash
   git commit -m "Description of your changes"
   ```

6. **Push Your Changes**:
   ```bash
   git push -u origin your-branch-name
   ```

7. **Create a Pull Request**: Submit your changes for review.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Thank you for using BidSecure! Happy bidding!
