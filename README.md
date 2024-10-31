# Stock Checker and Cart Automation for Rossmann & Gratis
This Python script automates stock checking and cart addition for products on Rossmann and Gratis e-commerce websites. The script logs in to user accounts, checks the stock status of wishlist items, and adds in-stock items to the cart automatically. It runs in parallel for both websites.

## Features
- Automated Stock Checking: Continuously checks the availability of wishlist items.
- Cart Addition: Adds in-stock items directly to the cart.
- Parallel Execution: Simultaneous automation for both Rossmann and Gratis.
- Configurable Login Credentials: Uses credentials stored in a separate file.

## Technologies Used
- Python: Main language used for the automation.
- Selenium: For browser automation and web interaction.
- Threading: Enables parallel stock checking for Rossmann and Gratis.

## Prerequisites
To run this project, you need:
- Python 3.7+
- Required Python packages (installable via requirements.txt)
- A Rossmann and Gratis account

## Installation

1. Clone the repository:
```
git clone https://github.com/katlicia/stock-checker.git
cd stock-checker
```

2. Install dependencies:
```
pip install -r requirements.txt
```

4. Set up login credentials:
Create an account.py file in the root directory with your account credentials:
```
mail = 'your_email@example.com'
acc_password = 'your_password'
```

## Usage
Run the script using the command:

```
python main.py
```
(You need to handle reCAPTCHA by clicking the checkbox manually while gratis is in login state.)

## Script Functions
1. rossmann_login_and_check_wishlist(): Logs into Rossmann, navigates to the wishlist, checks stock, and adds items to the cart if available.
2. gratis_login_and_check_wishlist(): Logs into Gratis, navigates to the wishlist, checks stock, and adds items to the cart if available.
3. run_parallel_checks(): Runs both rossmann_login_and_check_wishlist and gratis_login_and_check_wishlist functions in parallel threads.

## Stock Checking Logic
- Rossmann:
  - Retrieves wishlist items.
  - Checks for "In stock" items and adds them to the cart if available.
  - Refreshes the page every 10 seconds to update stock status.
- Gratis:
  - Similar stock checking process with additional popup handling.
  - Refreshes the page every 10 seconds to update stock status.
  
## Contributing
1. Fork this repository.
2. Create a new branch: git checkout -b feature/YourFeature.
3. Commit your changes: git commit -m 'Add some feature'.
4. Push to the branch: git push origin feature/YourFeature.
5. Open a pull request.

## License
Distributed under the MIT License. See LICENSE for more information.
