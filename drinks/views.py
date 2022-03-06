from django.http       import JsonResponse
from django.views     import View
from django.db.models import Q

from drinks.models import Drink
# Create your views here.

class ProductsView(View):
    def get(self, request):

        drinks = Drink.objects.all()

        q = Q()

        category    = request.GET.get("category", None)  
        caffeine    = request.GET.get("caffeine", None)
        price_upper = request.GET.get("price_upper", 200000) 
        price_lower = request.GET.get("price_lower", 0) 
    
        if category:
            categories = category.split(',')
            q.add(Q(category__name__in = categories), Q.AND) 

        if caffeine:
            if caffeine     == "yes":
                q.add(Q(caffeine__gt=0), Q.AND)  
            elif caffeine == "no":
                q.add(Q(caffeine__exact=0), Q.AND) 
        
        q.add(Q(price__range = (price_lower, price_upper)),Q.AND)

        filtered_drinks = drinks.filter(q) 


        recently = request.GET.get("recently", None)
        rating   = request.GET.get("rating", None)    

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
            for drink in filtered_drinks:      
                review_count , drink_average_review = compute_reviews(drink)
                drink_and_average_rating[drink.name] = drink_average_review
            whole_data_list = [{
                "name" : drink.name,
                "price"  : drink.price,
                "average_rating" : drink_average_review,
                "review_count"  : review_count
            } for drink in filtered_drinks]
            return whole_data_list

        if recently:
            filtered_drinks = filtered_drinks.order_by('-updated_at')
            whole_data_list = make_whole_data_list(filtered_drinks)


        elif rating:
            drink_and_average_rating = {}
            for drink in filtered_drinks:      
                review_count , drink_average_review = compute_reviews(drink)
                drink_and_average_rating[drink.name] = drink_average_review
            sorted_dict = sorted(drink_and_average_rating.items(), key=lambda x: x[1], reverse=True)
            sorted_key_list = []
            for i in sorted_dict:
                sorted_key_list.append(i[0])
            whole_data_list = []
            for name in sorted_key_list:
                data_dict = {}
                drink = Drink.objects.get(name=name)
                data_dict["name"] = drink.name
                data_dict["price"] = drink.price
                data_dict["average_rating"] = drink_and_average_rating[name]
                data_dict["review_count"] = drink.review_set.all().count()
                whole_data_list.append(data_dict)

        else: 
            whole_data_list = make_whole_data_list(filtered_drinks)

        return JsonResponse({'message':whole_data_list}, status = 200)

      