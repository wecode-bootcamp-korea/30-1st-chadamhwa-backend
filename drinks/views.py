from itertools import product
import json
from nis import cat
import re
from this import d
from unicodedata import category
from unittest.util import sorted_list_difference

from django.http     import JsonResponse
from django.views   import View
from django.db.models import Q

from drinks.models import Drink, Category, DrinkImage
from users.models import User, Review
# Create your views here.

class ProductsView(View):
    def get(self, request):

        drinks = Drink.objects.all()

        q = Q()

        category = request.GET.get("category", None)   # 카테고리 여러개 올 수 있음  # GET으로 받고 split으로 나눠줘야함
        caffeine = request.GET.get("caffeine", None)
        price_upper = request.GET.get("price_upper", 300000)  # 원래 getlist 썼다가, 각 인자로 range만들때 index error 떠서 얘로 바꿈 
        price_lower = request.GET.get("price_lower", 0) 

      
        if category:
            categories = category.split(',')
            q.add(Q(category__name__in = categories), Q.AND)   # __exact는 정확히 # 왜 id값만 받는지 나는 이름으로 필터링 하고 싶은데  # __name 으로 바꿔주니 되긴됨
           

        if caffeine:
            if caffeine == "yes":
                q.add(Q(caffeine__gt=0), Q.AND)  #__gt 는 보다 큼 
            elif caffeine == "no":
                q.add(Q(caffeine__exact=0), Q.AND) # id 말고 다른 것으로 
        
        q.add(Q(price__range = (price_lower, price_upper)),Q.AND)

        filtered_drinks = drinks.filter(q) # 필터링까지 완료! 얘네를 가지고 오더링 해서 리턴해줘야 함 


        recently = request.GET.get("recently", None)
        rating = request.GET.get("rating", None)     # rating과 recently가 한번에 올 수 는 없음 

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
        
        def make_whole_data_list(filtered_drinks):
            drink_and_average_rating = {}
            for drink in filtered_drinks:      # 미리 리뷰 갯수와 평점평균 계산해줌(json에 넣어야 하니깐)
                review_count , drink_average_review = compute_reviews(drink)
                drink_and_average_rating[drink.name] = drink_average_review
            whole_data_list = []
            for drink in filtered_drinks:
                data_dict={}
                data_dict["name"] = drink.name
                data_dict["price"] = drink.price
                data_dict["average_rating"] = drink_average_review
                data_dict["review_count"] = review_count
                whole_data_list.append(data_dict)
            return whole_data_list

        if recently:
            filtered_drinks = filtered_drinks.order_by('-updated_at')
            whole_data_list = make_whole_data_list(filtered_drinks)


        elif rating:
            drink_and_average_rating = {}
            for drink in filtered_drinks:      # 미리 리뷰 갯수와 평점평균 계산해줌(json에 넣어야 하니깐)
                review_count , drink_average_review = compute_reviews(drink)
                drink_and_average_rating[drink.name] = drink_average_review
            sorted_dict = sorted(drink_and_average_rating.items(), key=lambda x: x[1], reverse=True)
            sorted_key_list = []
            for i in sorted_dict:
                sorted_key_list.append(i[0])   # 평균 평점 높은 순으로 키값 정렬해서 sorted_key_list에 넣음 
            whole_data_list = []
            for name in sorted_key_list:
                data_dict = {}
                drink = Drink.objects.get(name=name)
                data_dict["name"] = drink.name
                data_dict["price"] = drink.price
                data_dict["average_rating"] = drink_and_average_rating[name]
                data_dict["review_count"] = drink.review_set.all().count()
                whole_data_list.append(data_dict)

        else:  #정렬 요청 아무것도 없는 경우
            whole_data_list = make_whole_data_list(filtered_drinks)

        return JsonResponse({'message':whole_data_list}, status = 200)

        # lst = []
        # for i in filtered_drinks:
        #     lst.append(i.name)

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