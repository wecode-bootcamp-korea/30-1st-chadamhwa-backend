import json

from django.http     import JsonResponse
from django.views   import View

from drinks.models import Drink
# Create your views here.

class FilteringView(View):  
    def post(self, request):
        data     = json.loads(request.body)
        method  = data["method"]
        
        # class compute_review:
        #     drink_reviews = drink.review_set.all() 
        #         review_count  = drink_reviews.count() 
        #         sum_rating    = 0
        #         for review in drink_reviews:       
        #             sum_rating += review.rating
        #         if review_count == 0:              
        #             drink_average_review = 0
        #         elif review_count != 0:                 
        #             drink_average_review = sum_rating / review_count
        #         return review_count, drink_average_review


        if method == "recent":
            recently_ordered_queryset = Drink.objects.all().order_by('-updated_at')
            data_ordered_list = []
            for drink in recently_ordered_queryset:
                data_dict = {}
                data_dict["name"] = drink.name
                data_dict["price"] = drink.price
                drink_reviews = drink.review_set.all() 
                review_count  = drink_reviews.count() 
                sum_rating    = 0
                for review in drink_reviews:       
                    sum_rating += review.rating
                if review_count == 0:              
                    drink_average_review = 0
                elif review_count != 0:                 
                    drink_average_review = sum_rating / review_count
                data_dict["average_rating"] = drink_average_review
                data_dict["review_count"] = review_count
                data_ordered_list.append(data_dict)
            return JsonResponse({'message':data_ordered_list}, status=200) 

        elif method == "price":
            price_range                = data["price_range"] 
            qualified_drinks           = Drink.objects.filter(price__range=(price_range[0],price_range[1]+1))
            qualified_drinks_in_order = qualified_drinks.order_by('price')
            data_ordered_list = []
            for drink in qualified_drinks_in_order:
                data_dict = {}
                data_dict["name"] = drink.name
                data_dict["price"]  = drink.price
                drink_reviews = drink.review_set.all() 
                review_count  = drink_reviews.count() 
                sum_rating    = 0
                for review in drink_reviews:       
                    sum_rating += review.rating
                if review_count == 0:              
                    drink_average_review = 0
                elif review_count != 0:                 
                    drink_average_review = sum_rating / review_count
                data_dict["average_rating"] = drink_average_review
                data_dict["review_count"] = review_count
                data_ordered_list.append(data_dict)
            return JsonResponse({'message':data_ordered_list}, status=200)
         
        elif method == "reviews": 
            drinks = Drink.objects.all()
            drink_and_average_rating = {}
            for drink in drinks:
                drink_reviews = drink.review_set.all() 
                review_count  = drink_reviews.count() 
                sum_rating    = 0
                for review in drink_reviews:       
                    sum_rating += review.rating
                if review_count == 0:              
                    drink_average_review = 0
                elif review_count != 0:                 
                    drink_average_review = sum_rating / review_count
                drink_and_average_rating[drink.name] = drink_average_review
            sorted_dict = sorted(drink_and_average_rating.items(), key=lambda x: x[1], reverse=True) 

            sorted_key_list= []
            for i in sorted_dict:
                sorted_key_list.append(i[0])
            data_ordered_list = []
            for name in sorted_key_list:
                data_dict = {}
                drink = Drink.objects.get(name=name)
                data_dict["name"] = drink.name
                data_dict["price"] = drink.price
                data_dict["average_rating"] = drink_and_average_rating[name]
                data_dict["review_count"] = drink.review_set.all().count()
                data_ordered_list.append(data_dict)
            return JsonResponse({'message':data_ordered_list}, status=200) 




        elif method == "caffeine":
            if data["caffeine"] == "caffeinated":
                drinks = Drink.objects.all()
                caffein_drinks  = drinks.filter(caffeine__range =(1,10000)).order_by('caffeine')
                data_ordered_list = []
                for drink in caffein_drinks:
                    data_dict = {}
                    data_dict["name"] = drink.name
                    data_dict["price"]  = drink.price
                    drink_reviews = drink.review_set.all() 
                    review_count  = drink_reviews.count() 
                    sum_rating    = 0
                    for review in drink_reviews:       
                        sum_rating += review.rating
                    if review_count == 0:              
                        drink_average_review = 0
                    elif review_count != 0:                 
                        drink_average_review = sum_rating / review_count
                    data_dict["average_rating"] = drink_average_review
                    data_dict["review_count"] = review_count
                    data_ordered_list.append(data_dict)
                return JsonResponse({'message':data_ordered_list}, status=200)
            
            elif data["caffeine"] == "decaffeinated":
                drinks = Drink.objects.all()
                decaffein_drinks    = drinks.filter(caffeine = 0)
                data_ordered_list = []
                for drink in decaffein_drinks:
                    data_dict = {}
                    data_dict["name"] = drink.name
                    data_dict["price"]  = drink.price
                    drink_reviews = drink.review_set.all() 
                    review_count  = drink_reviews.count() 
                    sum_rating    = 0
                    for review in drink_reviews:       
                        sum_rating += review.rating
                    if review_count == 0:              
                        drink_average_review = 0
                    elif review_count != 0:                 
                        drink_average_review = sum_rating / review_count
                    data_dict["average_rating"] = drink_average_review
                    data_dict["review_count"] = review_count
                    data_ordered_list.append(data_dict)
                return JsonResponse({'message':data_ordered_list}, status=200)


