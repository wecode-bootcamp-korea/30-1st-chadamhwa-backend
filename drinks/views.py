import json

from django.http     import JsonResponse
from django.views   import View

from drinks.models import Drink
# Create your views here.

class FilteringView(View):  
    def post(self, request):
        data     = json.loads(request.body)
        method  = data["method"]

        if method == "recent":
            recently_ordered_queryset = Drink.objects.all().order_by('-updated_at')
            date_ordered_list = []
            for i in recently_ordered_queryset:
                date_ordered_list.append(i.name)
            return JsonResponse({'message':date_ordered_list}, status=200) 

        elif method == "price":
            price_range                = data["price_range"] 
            qualified_drinks           = Drink.objects.filter(price__range=(price_range[0],price_range[1]+1))
            qualified_drinks_in_order = qualified_drinks.order_by('price')
            lst = []
            for i in qualified_drinks_in_order:
                lst.append(i.name)
            return JsonResponse({'message':lst}, status=200)
         
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
            sorted_dict = sorted(drink_and_average_rating.items(), key=lambda x: x[1], reverse=True) #(키,값) 이렇게 정렬
            sorted_key_list= []
            for i in sorted_dict:
                sorted_key_list.append(i[0])

            return JsonResponse({'message':sorted_key_list}, status=200)

        elif method == "caffein":
            if data["caffeine"] == "caffeinated":
                drinks = Drink.objects.all()
                caffein_drinks  = drinks.filter(caffeine__range =(1,10000)).order_by('caffeine')
                caffein_drinks_list = []
                for drink in caffein_drinks:
                    caffein_drinks_list.append(drink.name)
                return JsonResponse({'message':caffein_drinks_list}, status=200)
            
            elif data["caffeine"] == "decaffeinated":
                drinks = Drink.objects.all()
                decaffein_drinks    = drinks.filter(caffeine = 0)
                decaffein_drinks_list = []
                for drink in decaffein_drinks:
                    decaffein_drinks_list.append(drink.name)
                return JsonResponse({'message':decaffein_drinks_list}, status=200)


