import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chadamhwa.settings") # or 30-1st~~~.settings
import django
django.setup()
import csv
from drinks.models import *
from users.models import *
from orders.models import *
CSV_PATH = '/Users/jieun/Desktop/vs_code/chadamhwa/sample.csv' #csv 경로 
# def create_dict():
    # with open(CSV_PATH) as in_file:
    #     data_reader = csv.DictReader(in_file)
        # return data_reader
        
def insert_images():
    with open(CSV_PATH) as in_file:
        data_reader = csv.DictReader(in_file)
        for row in data_reader:
            if not DrinkImage.objects.filter(image_url=row["drink_image"]).exists():
                DrinkImage.objects.create(image_url=row["drink_image"])
def insert_categories():   # 몇 종류 안되는데 굳이 이렇게 만들어줄 필요 있나?
    with open(CSV_PATH) as in_file:
        data_reader = csv.DictReader(in_file)
        for row in data_reader:
            if not Category.objects.filter(name=row["category_name"]).exists():
                Category.objects.create(name=row["category_name"])
def insert_farms():
    with open(CSV_PATH) as in_file:
        data_reader = csv.DictReader(in_file)
        for row in data_reader:
            if not Farm.objects.filter(name=row["farm_name"]).exists():
                Farm.objects.create(name=row["farm_name"], image_url=row["farm_image"])
def insert_drinks(): 
    with open(CSV_PATH) as in_file:
        data_reader = csv.DictReader(in_file)   
        for row in data_reader:
            if not Drink.objects.filter(name=row["name"]).exists():
                category = Category.objects.get(name=row["category_name"])
                image = DrinkImage.objects.get(image_url=row["drink_image"])
                farm = Farm.objects.get(name=row['farm_name'])
                Drink.objects.create(
                    category = category,
                    image = image,
                    farm = farm,
                    weight=row["weight"],
                    caffeine=row["caffeine"],
                    price=row["price"], 
                    name=row["name"])
def insert_users():
    with open(CSV_PATH) as in_file:
        data_reader = csv.DictReader(in_file)
        for row in data_reader:
            if not User.objects.filter(email=row["email"]).exists():
                User.objects.create(
                    username = row["username"],
                    email = row["email"],
                    password = row["password"],
                    address = row["address"]
                )
def insert_reviews():
    with open(CSV_PATH) as in_file:
        data_reader = csv.DictReader(in_file)
        for row in data_reader:
            user = User.objects.get(username=row["username"])
            if not Review.objects.filter(user_id=user.id):
                drink = Drink.objects.get(name=row["name"])
                Review.objects.create(
                    drink = drink,
                    user = user,
                    rating= row["rating"],
                    comment = row["comment"],
                )
def insert_carts():
    with open(CSV_PATH) as in_file:
        data_reader = csv.DictReader(in_file)
        for row in data_reader:
            drink = Drink.objects.get(name=row["name"])
            user = User.objects.get(email=row["email"])
            if not Cart.objects.filter(drink_id=drink.id, user_id=user.id).exists():
                Cart.objects.create(
                    drink = drink,
                    user = user,
                    quantity = row["quantity"]
                )
            else:
                Cart.objects.filter(drink_id=drink.id, user_id=user.id).update(drink=drink, user=user, quantity = row["quantity"])
insert_images()
insert_categories()
insert_farms()
insert_drinks()
insert_users()
insert_reviews()
insert_carts()
# def insert_order_status(): # 몇 종류 안되는데 굳이 이렇게 만들어줄 필요 있나?
#     create_dict()
#     for row in data_reader:
# def insert_orders():
# def insert_order_items():
