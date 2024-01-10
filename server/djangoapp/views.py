from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from .models import *
from .restapis import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
# ...
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)
# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...
def logout_request(request):
    context = {}
    if request.method == "GET":
        logout(request)
        return redirect("/djangoapp")
# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':  
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    dealer_names = []

    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/77a51e91-e5c9-4d42-9c81-0ed40fdb627d/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        
        # Concat all dealer's short name
       # dealer_names2 = ' '.join(dealer.short_name for dealer in dealerships)
        for dealer in dealerships:
            dealer_names.append(dealer)
            
       # Return a list of dealer short name
        context['dealerships'] = dealer_names

        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealerId, dealer_name):
    context = {}
    dealer_reviews = []

    if request.method == "GET":
        url = "https://d6f5d202.us-south.apigw.appdomain.cloud/api2/get-review?id={}".format(dealerId)
        reviews = get_dealer_reviews_from_cf(url, dealerId)

        for review in reviews:
            dealer_reviews.append(review)
        
        context = {
            "dealerId":dealerId,
            "dealer_name" : dealer_name,
            "reviews" : dealer_reviews
        }
        dealer_details = render(request, 'djangoapp/dealer_details.html', context)
        return dealer_details
# Create a `add_review` view to submit a review
# def add_review(request, dealerId):
# ...
def add_review(request, dealerId, dealer_name):
    url = 'https://us-south.functions.appdomain.cloud/api/v1/web/77a51e91-e5c9-4d42-9c81-0ed40fdb627d/review-package/get-review'
    cars = CarModel.objects.filter(dealer = dealerId)

    #user_name = User.objects.get(auth_user.name)
    context = {"dealer_name":dealer_name,"dealerId":dealerId, "cars":cars}

    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/add_review.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        data = request.POST
        username = data['name']
        dealerId = dealerId
        review_text = data['review']
        purchased = data['purchased']
        review = {
            "name": username,
            "dealership": dealerId,
            "review": review_text,
            "purchase": purchased
        }

        if data['purchased'] == 'true':
                car = get_object_or_404(CarModel, pk=data["car"])
                review['purchase_date'] = data['purchase_date']
                review['car_make'] = car.car_make.name
                review['car_name'] = car.car_name
                review['car_type'] =car.car_type
                review['car_year'] = car.year
        res = save_review(url, review)

        return redirect(     
            'djangoapp:dealer_details', dealerId=dealerId, dealer_name=dealer_name)