import json

from django.views         import View
from django.http          import JsonResponse
from utils.login_required import login_required
from users.models         import Review, User
from drinks.models        import Drink

class CommentView(View):
    @login_required
    def post(self, request):
        try:
            data    = json.loads(request.body)

            rating  = data['rating']
            comment = data['comment']
            user_id = request.user.id

            if Review.objects.filter(user_id=user_id).exists():
                return JsonResponse({'message':'리뷰는 한번만 쓸수 있음!'}, status=400)

            drink   = Drink.objects.get(name=data['drink']).id

            Review.objects.create(
                user_id  = user_id,
                drink_id = drink,
                rating   = rating,
                comment  = comment
            )

            return JsonResponse({'message':'review_posting_success'}, status=200)
        
        except KeyError:
            return JsonResponse({'message':'Key_error'}, status=400)

        except Drink.DoesNotExist:
            return JsonResponse({'message':'존재하지 않는 음료입니다.'}, status=400)

    def get(self, request):
        try:
            data    = json.loads(request.body)
            drink_id   = data['drink_id']
            reviews = Review.objects.all()
            result  = []
            for review in reviews:
                user = User.objects.get(id=review.user_id)

                if review.drink.id == drink_id:
                    result.append(
                        {
                            'user' : user.username,
                            'rating' : review.rating,
                            'comment' : review.comment,
                            'created_at' : str(review.created_at).split()[0],
                        }
                    )
            return JsonResponse({'review':result}, status=200)
        
        except KeyError:
            return JsonResponse({'message':'Key_error'}, status=400)

        except json.decoder.JSONDecodeError:
            return JsonResponse({'message':'json값을 입력하세요'}, status=400)

            


