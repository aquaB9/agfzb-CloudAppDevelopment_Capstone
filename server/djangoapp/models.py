from django.db import models
from django.utils.timezone import now

try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

from django.conf import settings
import uuid

# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=200, default="car_name")
    description = models.CharField(max_length=1200, default="Description")

    def __str__(self):
            return "Name: " + self.name + "," + \
                "Description: " + self.description


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    
    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    HYPER = 'hyper'
    TYPE = [
        (SEDAN, 'Sedan'),
        (SUV, 'Suv'),
        (WAGON, 'Wagon'),
        (HYPER, 'Hyper')
    ]

    car_make = models.ForeignKey(CarMake, null=True, on_delete=models.CASCADE)
    car_name = models.CharField(max_length=200, default="car_name")
    dealer = models.IntegerField(null=True)
    car_type = models.CharField(null= False, max_length=20, choices= TYPE, default=SEDAN)
    year = models.IntegerField(default=1968)

    def __str__(self):
        return "Car: " + self.car_name + "," + \
               "Type: " + self.car_type

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_name, car_type, car_year, id, sentiment, createdAt):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_name = car_name
        self.car_type = car_type
        self.car_year = car_year
        self.id = id
        self.sentiment = sentiment
        self.createdAt = createdAt

    def __str__(self):
        return "Dealer name: " + self.name