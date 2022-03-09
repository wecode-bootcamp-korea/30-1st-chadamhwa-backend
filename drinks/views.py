from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q, Avg, Count

from drinks.models import Drink, Farm

#검색 기능 위한 전역변수
q_for_search = None


#ㅇㅇ        


class FarmProductsView(View):
    def get(self, request):


        #여기부터
        search_query    = request.GET.get('search_query', None)
        
        if search_query:
            global q_for_search
            q_for_search = Q(name__contains=search_query), Q.AND


        #여기까지는 검색기능 시도 
        
        farms = Farm.objects.all()

        farms_name_dic = {farm.name: [{

            "name"           : drink.name,
            "price"          : drink.price,
            "average_rating" : drink.average_rating,
            "review_count"   : drink.review_count,
            "image"          : drink.drinkimage_set.all()[0].thumb_img 

        }for drink in farm.drink_set.all().annotate(average_rating = Avg('review__rating'), review_count=Count('review')).order_by('-average_rating')[:4]] for farm in farms}

        return JsonResponse({'result':farms_name_dic}, status = 200)


class ProductsView(View):
    def get(self, request):
        #다른페이지검색기능



        #ㅇㅇㅇㅇㅇ
        q = Q()

        category        = request.GET.getlist("category", None)  
        is_caffeinated  = request.GET.get("is_caffeinated", None)
        price_upper     = request.GET.get("price_upper", 200000) 
        price_lower     = request.GET.get("price_lower", 0)
        search_query    = request.GET.get('search_query', None) 

        if search_query:
            global q_for_search
            q.add(q_for_search)

            #q.add(Q(name__contains=search_query), Q.AND)
        
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
            "name"           : drink.name,
            "price"          : drink.price,
            "average_rating" : drink.average_rating if drink.average_rating else 0,
            "review_count"   : drink.review_count,
            "image"          : drink.drinkimage_set.all()[0].thumb_img 
        }for drink in drinks.order_by(sort_by_options[sort_by])]

        return JsonResponse({'result':result}, status = 200)

