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

        q = Q()

        category = request.GET.get("category", None)  
        caffeine = request.GET.get("caffeine", None)
        price = request.GET.getlist("price", None)   #리스트 형태로 값이 들어옴 . 따라서 filter 적용시 __in 써줘야 함
        

        if category:
            q.add(Q(category__name= category), Q.AND)   # __exact는 정확히 # 왜 id값만 받는지 나는 이름으로 필터링 하고 싶은데  # __name 으로 바꿔주니 되긴됨

        if caffeine:
            if caffeine > 0:
                q.add(Q(caffeine__gt=0), Q.AND)  #__gt 는 보다 큼 
            elif caffeine == 0:
                q.add(Q(caffeine__exact=0), Q.AND) # id 말고 다른 것으로 
        
        filtered_drinks = drinks.filter(q)
        lst = []
        for i in filtered_drinks:
            lst.append(i.name)

        return JsonResponse({'message':lst}, status = 200)

        # if min_price and max_price:
        #     q &= Q()

        # cha_type / caffeinated / min_price & max_price

        # keys = []
        # for key in data.keys():
        #     keys.append(key)
        
        # values = []
        # for value in data.values():
        #     values.append(value)
        
        # q = Q()

        # for i in range(len(keys)):
        #     kei = keys[i]
        #     value = values[i] 
        #     q.add(Q(category=value), q.AND)

        # filtered_drinks = drinks.filter(q)

        # return JsonResponse({'message':filtered_drinks[0].name}, status = 200)



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