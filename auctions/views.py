from django.contrib.auth import authenticate, login, logout
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *
from . import forms
from django.contrib import messages
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.db import IntegrityError


def index(request):
    listings = Listing.objects.filter(active="True")
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def new_listing(request):
    ''' function where the user can add new listing. '''
    # when submit a form
    if request.method == "POST":
        form = forms.NewListingForm(request.POST)
        user_id = User.objects.get(pk=request.user.id)
        # check if valid
        if form.is_valid():
            # get listing's informations
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            category_id = form.cleaned_data["category"]
            category = Category.objects.get(pk=category_id)
            start_bid = form.cleaned_data["start_bid"]
            image = form.cleaned_data["image"]

            #insert the new listing to listing table
            new_entry = Listing.objects.create(
                title=title,
                listing_category=category,
                description=description,
                start_bid=start_bid,
                picture=image,
                user=user_id
            )
            new_entry.save()

        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/new_listing.html", {
        "form": forms.NewListingForm()
    })


def listing_page(request, id):
    ''' function take users to a page specific to a listing.'''

    # get the existing ids for the listings
    if not Listing.objects.filter(id=id).exists():
        return HttpResponseNotFound(render_to_string("auctions/error.html", {
                "message": "Listing doesn't exist."
                
            }))
    listing = Listing.objects.get(id=id)
    if listing.active:
        
        # get comments on the listing
        comments = Comment.objects.filter(listing=id)
       
        # if user loggedin
        if request.user.is_authenticated:
            # get owener
            owner_listing = Listing.objects.filter(user_id=request.user.id, id=id)

            # get user's watchlist
            listing_ids = (Watchlist.objects.filter(user=request.user.id).values_list('listing', flat=True))

            return render(request, "auctions/listing_page.html", {
                "listing": listing ,
                "listing_ids": listing_ids,
                "bid_form": forms.BidForm(),
                "comment_form": forms.CommentForm(),
                "comments": comments,
                "owner_listing": owner_listing.exists()
                
            })
        
        # get the listing
        return render(request, "auctions/listing_page.html", {
        "listing": listing,
        "comments": comments
        
        })
    # if listing closed and there is a winner
    elif Bids.objects.filter(listing=listing, is_winner=True):
        
        # get the winner
        winner = Bids.objects.get(listing=listing, is_winner=True)
        # if user is winner:
        if request.user.id == winner.user_id:
            messages.info(request, ('You won the bid'))
        # if the owener or any user made bid on the listing
        elif (request.user.id == listing.user_id or
                request.user.id in Bids.objects.filter(listing=listing).values_list('user_id', flat=True)): 
            messages.info(request, (f'The winner is {winner.user}'))
        else:
            # when the listing is closed
            messages.error(request, ('No longer available'))  
    else:
        # when the listing is closed with no bids
        messages.error(request, ('No longer available'))   
   
    return redirect("index")
   

@login_required
def add_remove_Watchlist(request, listing_id):
    '''function to add or remove items to/ from watchlist.'''
    
    # when user wants to add item to watchlist
    if request.POST.get('submit') == "Add to Watchlist":
        item = Watchlist()
        item.user_id = request.user.id
        item.listing_id = listing_id
        item.save()
    # when user wants to remove item from watchlist
    else:
        Watchlist.objects.get(listing=listing_id, user=request.user.id).delete()
    return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)))


@login_required
def bid(request, listing_id):
    '''fuction allows users to bid on listings'''
    
    if request.method == "POST":
        form = forms.BidForm(request.POST)  
        # check if valid
        if form.is_valid():
            # get the bid from data submited
            bid = form.cleaned_data['bid']
            # get the start bid for the listing
            listing = Listing.objects.get(pk=listing_id)
            start_bid = listing.start_bid
            
            # get highest bid from bids table
            highest_bid = Bids.objects.filter(listing=listing_id).aggregate(Max('user_bid'))['user_bid__max']
           
            # check if the bid is lower than start bid
            if (highest_bid and float(bid) <= float(highest_bid)) or float(bid) < float(start_bid):
                messages.error(request, ('Unvalid bid'))
            
                return redirect('listing_page', id=listing_id)
                
            # add new bid to database
            new_bid = Bids(user_bid=bid, listing=listing)
            new_bid.user_id = request.user.id
            new_bid.save()

            # update listing model
            listing.highest_bid = bid
            listing.save()

            # add the listing the user bid on it in his watchlist 
            if not Watchlist.objects.filter(user_id=request.user.id, listing=listing):
                item = Watchlist(user_id=request.user.id, listing=listing)
                item.save()
            
    return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)))


@login_required
def comment(request, listing_id):
    '''function allows users to add comments to listings'''

    if request.method == "POST":
        form = forms.CommentForm(request.POST)  
        # check if valid
        if form.is_valid():
            comment = form.cleaned_data['comment']
            add_to_comment = Comment(user_comment=comment)
            add_to_comment.user_id = request.user.id
            add_to_comment.listing_id = listing_id
            add_to_comment.save()
    return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)))


@login_required
def close_auction(request, listing_id):
    '''function allows the owener of the listing to close the auction'''
    
    # when owener close auction
    if request.POST.get("submit") == "close the auction":
        if Listing.objects.filter(user_id=request.user.id, id=listing_id).exists():

            # close listing
            listing = Listing.objects.get(pk=listing_id)
            listing.active = False
            listing.save()
            # get the winner bid
            if Bids.objects.filter(listing=listing_id):
                winner = Bids.objects.filter(listing=listing_id).order_by('user_bid').last()
                winner.is_winner = True
                winner.save()
          
    return redirect("index")


@login_required
def view_watchlist(request):
    watchlist = Watchlist.objects.filter(user_id=request.user.id).values_list('listing')
    
    watchlist_items = Listing.objects.filter(id__in=watchlist)
    
    return render(request, "auctions/watchlist.html", {
        "listings": watchlist_items
    })


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })


def category(request, category_id):
    listings = Listing.objects.filter(listing_category=category_id, active="True")
    return render(request, "auctions/category.html", {
        "listings": listings,
        "category" : Category.objects.get(pk=category_id)
    })
