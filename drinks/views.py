import json
from sys import api_version

from django.http     import JsonResponse
from django.views   import View

from drinks.models import Drink, Category, DrinkImage
from users.models import User, Review
# Create your views here.

class ProductsView(View):
    


    def get(self, request):
        # data     = request.GET #쿼리 스트링 전체를 가져옴    
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
        drinks_list = []
        for drink in drinks:
            review_count, average_rating = compute_reviews(drink)
            data_dict = {}
            data_dict["name"] = drink.name
            data_dict["price"] = drink.price
            data_dict["average_rating"] = average_rating
            data_dict["review_count"] = review_count
            data_dict["image"] = drink.image.image_url #일대일은 _set안쓰고 테이블에 연결된 컬럼명으로 바로 연결, 일대일이라 all() 도 안됨
            drinks_list.append(data_dict)
        return JsonResponse({'message':drinks_list}, status = 200)
