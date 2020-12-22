from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from datetime import datetime
from django.contrib.auth.decorators import login_required

from .models import User, AuctionListings, Bids, Comments, Watchlist, Closedbid, Alllisting

class Post(forms.Form):
    title = forms.CharField(label= "Title")
    textarea = forms.CharField(widget=forms.Textarea(), label='')
    bidamount = forms.IntegerField()
    category = forms.CharField(label="Category")
    link = forms.CharField(label="Image")

def index(request):
    items=AuctionListings.objects.all()
    try:
        w = Watchlist.objects.filter(user=request.user.username)
        wcount=len(w)
    except:
        wcount=None
    return render(request, "auctions/index.html",{
        "items":items
    })
    
def create(request):
    try:
        w = Watchlist.objects.filter(user=request.user.username)
        wlcount=len(w)
    except:
        wlcount=None
    if request.method == "GET":
        return render(request, "auctions/create.html", {
            "post": Post()
        })
    else:
        form = Post(request.POST)
        title = request.POST.get('title')
        desc = request.POST.get('textarea')
        category = request.POST.get('category')
        price = request.POST.get('bidamount')
        owner = request.user.username
        link = request.POST.get('link')
        listings = list(AuctionListings.objects.all())
        newlisting = AuctionListings.objects.create(title=title, desc=desc, category = category, price=price, link = link, owner = owner)
        listings = listings.append(newlisting)
        all = Alllisting()
        items = AuctionListings.objects.all()
        for i in items:
            try:
                if Alllisting.objects.get(listingid=i.id):
                    pass
            except:
                all.listingid=i.id
                all.title = i.title
                all.description = i.desc
                all.link = i.link
                all.save()
        return render(request, "auctions/index.html", {
            "items" : listings,
            "wlcount": wlcount
        })

def categories(request):
    items= AuctionListings.objects.raw("SELECT * FROM auctionlistings GROUP BY category")
    try:
        w = Watchlist.objects.filter(user=request.user.username)
        wlcount=len(w)
    except:
        wlcount=None
    return render(request,"auctions/categoriespage.html",{
        "items": items,
        "wlcount": wlcount 
    })
def category(request, category):
    categoryitems = AuctionListings.objects.filter(category=category)
    try:
        w = Watchlist.objects.filter(user=request.user.username)
        wlcount=len(w)
    except:
        wlcount=None
    return render(request,"auctions/category.html",{
        "items":categoryitems,
        "category":category,
        "wlcount" : wlcount
    })

def listingpage(request, id): 
    try:
        item = AuctionListings.objects.get(id=id)
    except:
        return redirect('index')

    try:
        comments = Comments.objects.filter(listingid=id)
    except:
        comments = None

    if request.user.username:
        try:
            if Watchlist.objects.get(user=request.user.username,listingid=id):
                added=True
        except:
            added = False
        try:
            l = AuctionListings.objects.get(id=id)
            if l.owner == request.user.username :
                owner=True
            else:
                owner=False
        except:
            return redirect('index')
    else:
        added=False
        owner=False
        try:
            wl = Watchlist.objects.filter(user=request.user.username)
            wlcount=len(wl)
        except:
            wlcount=None

    try:
        w = Watchlist.objects.filter(user=request.user.username)
        wlcount=len(w)
    except:
        wlcount=None
    return render(request,"auctions/listingpage.html", { 
            "item":item,
            "added": added,
            "owner": owner,
            "comments": comments,
            "error":request.COOKIES.get('error'),
            "successgreen":request.COOKIES.get('successgreen'),
            "wlcount": wlcount
        })

def bidsubmit(request, listingid):
    cur_bid = AuctionListings.objects.get(id=listingid)
    current_bid = cur_bid.price

    if request.method == "POST":
        user_bid = int(request.POST.get("bid"))
        if user_bid > current_bid:
            listing_items = AuctionListings.objects.get(id=listingid)
            listing_items.price = user_bid
            listing_items.save()
            try:
                if Bids.objects.filter(id=listingid):
                    bidrow = Bids.objects.filter(id=listingid)
                    bidrow.delete()
                b = Bids()
                b.bidamount = user_bid
                b.bidderinfo = request.user.username
                b.listingid = listingid
                b.save() 
            except:
                b = Bids()
                b.bidamount = user_bid
                b.bidderinfo = request.user.username
                b.listingid = listingid
                b.save() 
            response = redirect('listingpage',id=listingid)
            response.set_cookie('successgreen','Bid Successful!',max_age=3)
            return response
        else :
            response = redirect('listingpage',id=listingid)
            response.set_cookie('error','Bid should be greater than the current price',max_age=3    )
            return response   
    else :
        return redirect('index')

def closebid(request, listingid):
    if request.user.username:
        try:
            listingrow = AuctionListings.objects.get(id=listingid)
        except: 
            return redirect('index')
        cb = Closedbid()
        title = listingrow.title
        cb.owner = listingrow.owner
        cb.listingid = listingid
        try:
            bidrow = Bids.objects.get(listingid=listingid, bidamount=listingrow.price)
            cb.winner = bidrow.bidderinfo
            cb.winningprice = bidrow.bidamount
            cb.save()
            bidrow.delete()
        except:
            cb.winner = listingrow.owner
            cb.winningprice = listingrow.price
            cb.save() 
        try:
            if Watchlist.objects.filter(listingid=listingid):
                watchrow = Watchlist.objects.filter(listingid=listingid)
                watchrow.delete()
            else:
                pass
        except:
            pass
        try:
            crow = Comments.objects.filter(listingid=listingid)
            crow.delete()
        except:
            pass
        try:
            brow = Bids.objects.filter(listingid=listingid)
            winner = bidrow.bidderinfo
            brow.delete()
        except:
            pass
        try:
            cblist=Closedbid.objects.get(listingid=listingid)
        except:
            cb.owner = listingrow.owner
            cb.winner = winner
            print("getting bid info - owner 3")
            print(cb.winner)
            cb.listingid = listingid
            cb.winningprice = listingrow.price
            cb.save()
            cblist=Closedbid.objects.get(listingid=listingid)
        listingrow.delete()
        try:
            w = Watchlist.objects.filter(user=request.user.username)
            wlcount=len(w)
        except:
            wlcount=None
        return render(request,"auctions/winningpage.html",{
            "cb":cblist,
            "title":title,
            "wlcount":wlcount
        })   
    else:
        return redirect('index') 
def commentsubmit(request,listingid):
    if request.method == "POST":
        now = datetime.now()
        dt = now.strftime(" %d %B %Y %X ")
        c = Comments()
        c.comment = request.POST.get('comment')
        c.user = request.user.username
        c.time = dt
        c.listingid = listingid
        c.save()
        return redirect('listingpage',id=listingid)
    else :
        return redirect('index')

def addwatchlist(request, listingid):
    if request.user.username: 
        wl = Watchlist()
        wl.user = request.user.username
        wl.listingid = listingid
        wl.save()
        return redirect('listingpage',id=listingid)
    else:
        return redirect('index')
def removewatchlist(request, listingid):
    if request.user.username:
        try: 
            wl = Watchlist.objects.get(user= request.user.username, listingid = listingid)
            wl.delete()
            return redirect('listingpage',id=listingid)
        except:
            return redirect('listingpage',id=listingid)
    else:
        return redirect('index')

def watchlistpage(request, username):
    if request.user.username:
        try:
            try:
                wl = Watchlist.objects.filter(user= username)
                wlcount=len(wl)
            except:
                wlcount: None    
            
            items=[]

            for item in wl:
                items.append(AuctionListings.objects.filter(id = item.listingid))
            return render(request,"auctions/watchlistpage.html",{
                "items":items,
                "wlcount":wlcount
            })
        except:
            try:
                wl = Watchlist.objects.filter(user=request.user.username)
                wlcount=len(wl)
            except:
                wlcount=None
            return render(request,"auctions/watchlistpage.html",{
                "items":None,
                "wlcount":wlcount
            })
    else: 
        return redirect('index')

def mywins(request):
    print("USERNAME")
    if request.user.username:
        print("USERNAME 1")
        items=[]
        try:
            wonitems = Closedbid.objects.filter(winner=request.user.username)
            for w in wonitems:
                items.append(Alllisting.objects.filter(listingid=w.listingid))
        except:
            wonitems = None
            items = None
        try:
            wl = Watchlist.objects.filter(user=request.user.username)
            wlcount=len(wl)
        except:
            wlcount=None
        return render(request,'auctions/mywins.html',{
            "items":items,
            "wcount":wlcount,
            "wonitems":wonitems
        })
    else:
        return redirect('index')

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        listings = []
        names=[] 
        # Check if authentication successful
        if user is not None:
            
            login(request, user)
            #for a in AuctionListings.objects.all():
            #    if a is not None:   
            #        names.append(a.name)
            listings = list(AuctionListings.objects.all())
            return render(request, "auctions/index.html", {
                "items" : listings
            })
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
