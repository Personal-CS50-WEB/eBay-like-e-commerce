from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("<int:id>", views.listing_page, name="listing_page"),
    path("add_remove_Watchlist/<int:listing_id>", views.add_remove_Watchlist, name="add_remove_Watchlist"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("close_auction/<int:listing_id>", views.close_auction, name="close_auction"),
    path("view_watchlist", views.view_watchlist, name="view_watchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>", views.category, name="category"),

]
