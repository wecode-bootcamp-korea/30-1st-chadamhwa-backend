from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

from drinks.models import Drink
from drinks.utils import whole_data_list_with_review, compute_reviews

class ProductsView(View):
    def get(self, request):

        drinks = Drink.objects.all()

        q = Q()

        category    = request.GET.getlist("category", None)  
        caffeine    = request.GET.get("caffeine", None)
        price_upper = request.GET.get("price_upper", 200000) 
        price_lower = request.GET.get("price_lower", 0) 
    
        if category:
            categories = category[0].split(',')
            q.add(Q(category__name__in = categories), Q.AND) 

        if caffeine != None :
            if caffeine == True: # 0초과    # if ~ else 둘다 caffein 0 인애들 나옴
                q.add(Q(caffeine__gt=0), Q.AND)  
            else:  #
                q.add(Q(caffeine__exact=0), Q.AND) 
            
        q.add(Q(price__range = (price_lower, price_upper)),Q.AND)

        filtered_drinks = drinks.filter(q) 



        newest = request.GET.get("newest", None)
        rating   = request.GET.get("rating", None)    

        if newest:
            filtered_drinks = filtered_drinks.order_by('-updated_at')
            whole_data_list = whole_data_list_with_review(filtered_drinks)
# annotate 메소드 - 가상의 칼럼 -  average
# 삼항연산자

        elif rating:
            drink_and_average_rating = {}
            for drink in filtered_drinks:      
                drink_average_review = compute_reviews(drink)
                drink_and_average_rating[drink.name] = drink_average_review
            sorted_dict = sorted(drink_and_average_rating.items(), key=lambda x: x[1], reverse=True)
            sorted_key_list = []
            for items in sorted_dict:
                sorted_key_list.append(items[0])
            whole_data_list = [{
                "name" : Drink.objects.get(name=name).name ,
                "price" : Drink.objects.get(name=name).price,
                "average_rating" : drink_and_average_rating[name],
                "review_count" : Drink.objects.get(name=name).review_set.all().count(),
                "image" : Drink.objects.get(name=name).image.image_url
            }for name in sorted_key_list ]

        else: 
            whole_data_list = whole_data_list_with_review(filtered_drinks)

        return JsonResponse({'message':whole_data_list}, status = 200)

      