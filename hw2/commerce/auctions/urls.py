from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.category, name="category"),
    path("watchList", views.watchList, name="watchList"),
    path("createListing", views.createListing, name="createListing"),

    path("listing/<int:auctionId>", views.listing, name="listing"),
    path("watchListing/<int:auctionId>", views.watchListing, name="watchListing"),
    path("stopWatching/<int:auctionId>", views.stopWatching, name="stopWatching"),
    path("closeAuction/<int:auctionId>", views.closeAuction, name="closeAuction"),
]
