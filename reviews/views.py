import json

from django.views         import View
from django.http          import JsonResponse
from utils.login_required import login_required
from users.models         import Review, User
from drinks.models        import Drink

class CommentView(View):
    @login_required
    def post(self, request, drink_id):
        try:
            data    = json.loads(request.body)

            rating  = data['rating']
            comment = data['comment']
            user_id = request.user.id
            drink   = Drink.objects.get(id=drink_id).id
        
            Review.objects.update_or_create(
                user_id  = user_id,
                drink_id = drink,
                defaults = {'comment':comment, 'rating':rating}
            )

            """
            user.id(1) = user_id(1) -->      T  T
            drink_id(2) = drink(2),  -->     T  T 
            
            defaults = {'comment': comment} 무시 무시  --> 비교할 때만
                                            생성 수정  --> default 도 포함
            디폴트를 제외한 값을 비교했을 때 하나라도 F 다 --> 생성
                                     모두 다 T 다 ---> 수정
            """

            return JsonResponse({'message':'review_posting_success'}, status=200)
        
        except KeyError:
            return JsonResponse({'message':'Key_error'}, status=400)


    def get(self, request, drink_id):
        try:
            reviews = Review.objects.all()
            result  = [
                {
                    'user' : User.objects.get(id=review.user_id).username,
                    'rating' : review.rating,
                    'comment' : review.comment,
                    'created_at' : str(review.created_at).split()[0]
                } 
                    for review in reviews if review.drink.id == drink_id
            ]
        
            return JsonResponse({'review':result}, status=200)
        
        except KeyError:
            return JsonResponse({'message':'Key_error'}, status=400)
            