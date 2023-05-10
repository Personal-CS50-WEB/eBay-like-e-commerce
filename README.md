# eBay-like-e-commerce

This is an auction site built using Django. 

## Installation
To install the necessary dependencies for this project, navigate to the root directory and run:

1. Clone the code: https://github.com/Personal-CS50-WEB/eBay-like-e-commerce.git
2. pip install -r requirements.txt
3. In the terminal, python manage.py makemigrations network to make migrations for the network app.
4. python manage.py migrate
5. python manage.py runserver pip install -r requirements.txt

## Functionality
### **Models**
The application has four models, including the User model. The other models are for auction listings, bids, and comments made on auction listings.

### **Create Listing**
Users can create a new listing by clicking on the "Create Listing" button and filling out the form. They can specify a title for the listing, a text-based description, and what the starting bid should be. Users can also provide a URL for an image for the listing and/or a category.

### **Active Listings Page**
The default route of the web application shows all currently active auction listings. For each listing, the page displays the title, description, current price, and photo (if one exists for the listing).

### **Listing Page**
Clicking on a listing takes users to a page specific to that listing. On that page, users can view all details about the listing, including the current price for the listing. If the user is signed in, the user can add the item to their “Watchlist.” If the item is already on the watchlist, the user can remove it. If the user is signed in, the user can bid on the item. The bid must be at least as large as the starting bid and greater than any other bids that have been placed (if any). If the bid doesn't meet those criteria, the user is presented with an error. If the user is signed in and is the one who created the listing, the user has the ability to "close" the auction from this page, which makes the highest bidder the winner of the auction and makes the listing no longer active. If a user is signed in on a closed listing page, and the user has won that auction, the page says so. Users who are signed in can add comments to the listing page. The listing page displays all comments that have been made on the listing.

### **Watchlist**
Users who are signed in can visit a Watchlist page, which displays all of the listings that a user has added to their watchlist. Clicking on any of those listings takes the user to that listing’s page.

### **Categories**
Users can visit a page that displays a list of all listing categories. Clicking on the name of any category takes the user to a page that displays all of the active listings in that category.

### **Django Admin Interface**
Via the Django admin interface, a site administrator can view, add, update, and delete listings, bids, comments, and categories.

## Conclusion
This concludes the overview of the E-commerce Auction Site. We hope you enjoy using our site!

