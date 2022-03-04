import json

from django.http     import JsonResponse
from django.views   import View

from drinks.models import Drink
# Create your views here.

class FilteringView(View):  
    def get(self, request):
        data     = request.GET #쿼리 스트링 전체를 가져옴 
        
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


        if data.get("ordering", None) == "-updated_at":
            recently_ordered_queryset = Drink.objects.all().order_by('-updated_at')
            data_ordered_list = []
            for drink in recently_ordered_queryset:
                data_dict = {}
                data_dict["name"] = drink.name
                data_dict["price"] = drink.price
                review_count , drink_average_review = compute_reviews(drink)
                data_dict["average_rating"] = drink_average_review
                data_dict["review_count"] = review_count
                data_ordered_list.append(data_dict)
            return JsonResponse({'message':data_ordered_list}, status=200) 

        elif data.get("Min_price", None) and data.get("max_price",None):
            price_range                = [int(data.get("Min_price", None)), int(data.get("max_price",None))]
            qualified_drinks           = Drink.objects.filter(price__range=(price_range[0],price_range[1]+1))
            qualified_drinks_in_order = qualified_drinks.order_by('price')
            data_ordered_list = []
            for drink in qualified_drinks_in_order:
                data_dict = {}
                data_dict["name"] = drink.name
                data_dict["price"]  = drink.price
                review_count , drink_average_review = compute_reviews(drink)
                data_dict["average_rating"] = drink_average_review
                data_dict["review_count"] = review_count
                data_ordered_list.append(data_dict)
            return JsonResponse({'message':data_ordered_list}, status=200)



        elif data.get("filtering", None) == "caffeinated":
            drinks = Drink.objects.all()
            caffein_drinks  = drinks.filter(caffeine__range =(1,10000)).order_by('caffeine')
            data_ordered_list = []
            for drink in caffein_drinks:
                data_dict = {}
                data_dict["name"] = drink.name
                data_dict["price"]  = drink.price
                review_count , drink_average_review = compute_reviews(drink)
                data_dict["average_rating"] = drink_average_review
                data_dict["review_count"] = review_count
                data_ordered_list.append(data_dict)
            return JsonResponse({'message':data_ordered_list}, status=200)
            
        elif data.get("filtering", None) == "decaffeinated":
            drinks = Drink.objects.all()
            decaffein_drinks    = drinks.filter(caffeine = 0)
            data_ordered_list = []
            for drink in decaffein_drinks:
                data_dict = {}
                data_dict["name"] = drink.name
                data_dict["price"]  = drink.price
                review_count , drink_average_review = compute_reviews(drink)
                data_dict["average_rating"] = drink_average_review
                data_dict["review_count"] = review_count
                data_ordered_list.append(data_dict)
            return JsonResponse({'message':data_ordered_list}, status=200)

        elif data.get("ordering", None) == "-ratings":
            drinks = Drink.objects.all()
            drink_and_average_rating = {}
            for drink in drinks:
                review_count , drink_average_review = compute_reviews(drink)
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

