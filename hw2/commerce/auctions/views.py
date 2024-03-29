from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
from datetime import timedelta
from .models import User, Auction, Bid, Comment
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from urllib.parse import unquote

def index(request):
    now = timezone.now()
    return render(request, "auctions/index.html", {
                "title": "Active Listings",
                "listings": Auction.objects.filter(endTime__gt = now).annotate(price=Max('bids__price'))
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
def createListing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        category = request.POST["category"]
        imageUrl = request.POST["imageUrl"]
        openingBid = float(request.POST["openingBid"]) * 100
        
        # TODO do some cheking

        try:
            newAuction = Auction(title=title, description=description, imagePath=imageUrl, category=category, openingPrice= openingBid, creator= request.user)
            newAuction.startTime = timezone.now()
            newAuction.endTime = newAuction.startTime + timedelta(weeks=1)
            newAuction.save()
        except IntegrityError:
            return render(request, "auctions/index.html", {
                "message": "Some Error Happened"
            })
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/createListing.html", {
                "message": "No message"
            })

@login_required
def watchList(request):
    user = User.objects.get(pk=request.user.id)
    return render(request, "auctions/index.html", {
                "title": "Watchlist",
                "listings": user.watchlist.all()
            })

def categories(request):
    cats = ["asd", "asd", "asd"]
    return render(request, "auctions/categories.html", {
                "categories": Auction.objects.values("category").distinct().all()
            })

def category(request, category):
    now = timezone.now()
    category = unquote(category)

    return render(request, "auctions/index.html", {
                "title": "Category: " + category,
                "listings": Auction.objects.filter(category = category, endTime__gt = now)
            })
    

def listing(request, auctionId):
    auction = Auction.objects.get(pk = auctionId)

    try:
        maxBid = auction.bids.latest('price')
    except:
        maxBid = None


    isWatched = False
    if request.user.is_authenticated:
        isWatched = auction.watched_by.filter(username= request.user.get_username()).exists()
    
    if request.method == "POST":
        if 'bid' in request.POST:
            print("It came to bids")
            bid = float(request.POST["bid"]) * 100
            # TODO do some cheking
            price = maxBid.price if maxBid != None else auction.openingPrice

            if price == None:
                price = auction.openingPrice

            if bid > price: 
                #valid bid, do things
                try:
                    user = User.objects.get(pk=request.user.id)
                    newBid = Bid(user = user, auction = auction, price = bid)
                    newBid.save()
                except IntegrityError:
                    return render(request, "auctions/listing.html", {
                        "auction": auction,
                        "maxBid": maxBid,
                        "isWatched": isWatched,
                        "message": "Some Error Happened. Code: VI127",
                        "comments": auction.comments.all()
                    })
                return HttpResponseRedirect(reverse("listing", kwargs={'auctionId':auctionId}))
                    
            else:
                return render(request, "auctions/listing.html", {
                        "auction": auction,
                        "isWatched": isWatched,
                        "maxBid": maxBid,
                        "message": "Your bid must be bigger than current price",
                        "comments": auction.comments.all()
                    })
    
        elif 'comment' in request.POST:
            print("Comment was: " + request.POST["comment"])
            text = request.POST["comment"]
            if len(text) < 3:
               return render(request, "auctions/listing.html", {
                    "auction": auction,
                        "isWatched": isWatched,
                        "maxBid": maxBid,
                        "message": "Comment shuold be at least 3 letters",
                        "comments": auction.comments.all()
                })
            try:
                user = User.objects.get(pk=request.user.id)
                newComment = Comment(user = user, auction = auction, text = text)
                newComment.save()
            except IntegrityError:
                return render(request, "auctions/listing.html", {
                    "auction": auction,
                        "isWatched": isWatched,
                        "maxBid": maxBid,
                        "message": "Some Error happened. Error No: VI166",
                        "comments": auction.comments.all()
                })
            return HttpResponseRedirect(reverse("listing", kwargs={'auctionId':auctionId}))
        else:
            return HttpResponseRedirect(reverse("listing", kwargs={'auctionId':auctionId}))

    if auction == None:
        return HttpResponseNotFound()
    else:
        return render(request, "auctions/listing.html", {
                "auction": auction,
                "maxBid": maxBid,
                "isWatched": isWatched,
                "comments": auction.comments.all()
            })

@login_required
def watchListing(request, auctionId):

    auction = Auction.objects.get(pk=auctionId)
    user = User.objects.get(username=request.user.get_username())

    user.watchlist.add(auction)

    return HttpResponseRedirect(reverse("listing", kwargs={'auctionId':auctionId}))


@login_required
def stopWatching(request, auctionId):

    auction = Auction.objects.get(pk=auctionId)
    user = User.objects.get(username=request.user.get_username())

    user.watchlist.remove(auction)

    return HttpResponseRedirect(reverse("listing", kwargs={'auctionId':auctionId}))

@login_required
def closeAuction(request, auctionId):

    auction = Auction.objects.get(pk=auctionId)
    auction.endTime = timezone.now()
    auction.save()

    return HttpResponseRedirect(reverse("listing", kwargs={'auctionId':auctionId}))
