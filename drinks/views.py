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

   # rating순으로 name 정렬까진 됐는데, 이 정렬된 아이들에 해당하는 instance를 통해서 name,price,평점평균,평점갯수를 딕셔너리에 담아서 리턴해줘야 함 

    
            # data_ordered_list = [] 
            # for i in sorted_key_list:
            #     data_dict = {}
            #     drink_inorder = drinks.get(name=i)
            #     data_dict["name"] = drink_inorder.name
            #     data_dict["price"] = drink_inorder.price
            #     drink_reviews = drink.review_set.all() 
            #     review_count  = drink_reviews.count() 
            #     sum_rating    = 0
            #     for review in drink_reviews:       
            #         sum_rating += review.rating
            #     if review_count == 0:              
            #         drink_average_review = 0
            #     elif review_count != 0:                 
            #         drink_average_review = sum_rating / review_count
            #     data_dict["average_rating"] = drink_inorder.drink_average_review
            #     data_dict["review_count"] = drink_inorder.reveiw.count
            #     data_ordered_list.append(data_dict)
            # return JsonResponse({'message':data_ordered_list}, status=200)




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


