from itertools import product
import json
from nis import cat
from this import d
from unicodedata import category

from django.http     import JsonResponse
from django.views   import View
from django.db.models import Q

from drinks.models import Drink, Category, DrinkImage
from users.models import User, Review
# Create your views here.

class ProductsView(View):
    def get(self, request):
           
        def compute_reviews(drink):
            drink_reviews = drink.review_set.all() 
            review_count  = drink_reviews.count() 
            sum_rating    = 0
            for review in drink_reviews:       
                sum_rating += review.rating
            if review_count == 0:              
                drink_average_review = 0
            elif review_count != 0:                 
                drink_average_review = sum_rating / review_count
            return review_count, drink_average_review

        drinks = Drink.objects.all()
        # drinks_list = []
        # for drink in drinks:
        #     review_count, average_rating = compute_reviews(drink)
        #     data_dict = {}
        #     data_dict["name"] = drink.name
        #     data_dict["price"] = drink.price
        #     data_dict["average_rating"] = average_rating
        #     data_dict["review_count"] = review_count
        #     data_dict["image"] = drink.image.image_url #일대일은 _set안쓰고 테이블에 연결된 컬럼명으로 바로 연결, 일대일이라 all() 도 안됨
        #     drinks_list.append(data_dict)
        # return JsonResponse({'message':drinks_list}, status = 200)

        data = request.GET #쿼리 스트링 전체를 가져옴 

        keys = []
        for key in data.keys():
            keys.append(key)
        
        values = []
        for value in data.values():
            values.append(value)
        
        q = Q()

        for i in range(len(keys)):
            kei = keys[i]
            value = values[i] 
            q.add(Q(category=value), q.AND)

        filtered_drinks = drinks.filter(q)

        return JsonResponse({'message':filtered_drinks[0].name}, status = 200)



        # category = data.get("category", None),
        # caffeinated = data.get("caffeine", None), # "caffein 있냐 또는 없냐 로 받고, 아무 값도 오지 않을시는 선택안된 것"
        # min_price = data.get("min_price", None),
        # max_price = data.get("max_price", None),
        # rating = data.get("rating", None),
        # latest = data.get("latest", None)
        
        # query_parameters = [category, caffeinated, min_price, max_price, rating, latest]
        # valued_parameters = []
        # for i in query_parameters:
        #     if i != None:
        #         valued_parameters.append(i)
        
        # for parameter in valued_parameters:
        #     drinks.filter

                

        