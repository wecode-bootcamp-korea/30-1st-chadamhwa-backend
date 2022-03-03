import json

from django.http import JsonResponse
from django.views import View

from drinks.models import Drink
# Create your views here.

class FilteringView(View):  # 최신순 , 가격순(range사용), 리뷰순 #처음에는 db에 들어있는대로 나열 
    def post(self, request):
        # try:
        data = json.loads(request.body)
        method = data["method"]

        if method == "recent":
            recently_ordered_list = Drink.objects.all().order_by('-updated_at') #생성시간이 아니라 업뎃시간 기준으로 만듬 
            lst = []
            for i in recently_ordered_list:
                lst.append(i.name)
            return JsonResponse({'message':lst}, status=200) #뭘 리턴해줘야 하는지, 객체냐 이름이냐 pk값이냐

        elif method == "price":
            price_range = data["price_range"] #프론트에서 리스트로 가격의 시작값과 끝값 보내줌
            qualified_drinks = Drink.objects.filter(price__range=(price_range[0],price_range[1]+1))
            qualified_drinks_in_order = qualified_drinks.order_by('price')
            lst = []
            for i in qualified_drinks_in_order:
                lst.append(i.name)
            return JsonResponse({'message':lst}, status=200)
         
            # drinks = Drink.objects.all()
            # qualified_drinks = []
            # for i in drinks:
            #     if i.price in range(price_range[0],price_range[1]+1):
            #         qualified_drinks.append(i.name)
            # for j in qualified_drinks:

        elif method == "reviews": # 리뷰 평점 높은 순 
            # drink_count = Drink.objects.count()  # drinks 전체 갯수(평균낼때 사용)
            drinks = Drink.objects.all()
            drink_and_average_rating = {}
            for drink in drinks:
                drink_reviews = drink.review_set.all() # 특정 drink를 정참조하는 리뷰들 전체의 인스턴스  
                review_count = drink_reviews.count() # 특정 drink의 리뷰 갯수
                sum_rating = 0
                for review in drink_reviews:        # drink에 해당하는 리뷰들 for문 돌림
                    sum_rating += review.rating
                if review_count == 0:               # division by zero 방지
                    drink_average_review = 0
                elif review_count != 0:                 # 0으로 나눠주는 경우 아닐 시 
                    drink_average_review = sum_rating / review_count
                drink_and_average_rating[drink.name] = drink_average_review
            sorted_dict = sorted(drink_and_average_rating.items(), key=lambda x: x[1], reverse=True)
            sorted_key_list= []
            for i in sorted_dict:
                sorted_key_list.append(i[0])

            return JsonResponse({'message':sorted_key_list}, status=200)


