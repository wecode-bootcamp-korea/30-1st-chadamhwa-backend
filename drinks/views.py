from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q, Avg, Count

from drinks.models import Drink, Farm

class ProductView(View):
    def get(self, request):
        
        q = Q()

        category        = request.GET.getlist("category", None)  
        is_caffeinated  = request.GET.get("is_caffeinated", None)
        price_upper     = request.GET.get("price_upper", 200000) 
        price_lower     = request.GET.get("price_lower", 0)
        search_query    = request.GET.get('search_query', None) 

        if search_query:
            q.add(Q(name__contains=search_query), Q.AND)
        
        if category:
            categories = category[0].split(',')
            q.add(Q(category__name__in = categories), Q.AND) 

        if is_caffeinated:
            q.add(Q(caffeine__gt=0), Q.AND) if is_caffeinated=="True" else q.add(Q(caffeine__exact=0), Q.AND) 

        q.add(Q(price__range = (price_lower, price_upper)),Q.AND)

        drinks = Drink.objects.filter(q).annotate(average_rating = Avg('review__rating'), review_count=Count('review'))

        sort_by = request.GET.get('sort_by', None)
        
        sort_by_options = {
            "newest"         : "-updated_at",
            "oldest"         : "updated_at",
            "highest_rating" : "-average_rating",
        }

        result = [{
            "id"              : drink.id,
            "name"           : drink.name,
            "price"          : drink.price,
            "average_rating" : drink.average_rating if drink.average_rating else 0,
            "review_count"   : drink.review_count,
            "image"          : drink.drinkimage_set.all().first().thumb_img 
        }for drink in drinks.order_by(sort_by_options[sort_by])]

        return JsonResponse({'result':result}, status = 200)


class FarmProductView(View):
    def get(self, request):
                
        offset          = request.GET.get("offset", 0)
        limit           = request.GET.get("limit", 4)
        order_method    = request.GET.get("order_method", "highest_rating")

        order_method_options = {
            "highest_rating" : "-average_rating",
            "newest"         : "-updated_at",
            "oldest"         : "updated_at"  
        }

        farms = Farm.objects.all()

        result = {
                "farm" : [{
                    "id"       : farm.id,
                    "name"  : farm.name,
                    "drinks" : [
                        {
                            "id"             : drink.id,
                            "name"           : drink.name,
                            "price"          : drink.price,
                            "average_rating" : drink.average_rating,
                            "review_count"   : drink.review_count,
                            "image"          : drink.drinkimage_set.all().first().thumb_img,
                        }  for drink in farm.drink_set.all().annotate(average_rating = Avg('review__rating'), review_count=Count('review'))\
                            .order_by(order_method_options[order_method])[offset:offset+limit]]
            } for farm in farms]
        }

        return JsonResponse({'result':result}, status = 200)


  
  
