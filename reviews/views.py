import json

from django.views         import View
from django.http          import JsonResponse
from utils.login_required import login_required
from users.models         import Review, User
from drinks.models        import Drink
from django.db.models     import Avg

class CommentView(View):
    @login_required
    def post(self, request, drink_id):
        try:
            data    = json.loads(request.body)

            rating  = data['rating']
            comment = data['comment']
            user_id = request.user.id
            drink   = Drink.objects.get(id=drink_id)
        
            Review.objects.update_or_create(
                user_id  = user_id,
                drink = drink,
                defaults = {'comment':comment, 'rating':rating}
            )

            return JsonResponse({'message':'review_posting_success'}, status=201)
        
        except KeyError:
            return JsonResponse({'message':'Key_error'}, status=400)


    def get(self, request, drink_id):
        reviews = Review.objects.all()
        result  = [
            {
                'user'              : User.objects.get(id=review.user_id).username,
                'rating'            : review.rating,
                'comment'           : review.comment,
                'created_at'        : review.created_at.date(),
                'thumb_img'         : Drink.objects.get(id=review.drink_id).drinkimage_set.get(drink_id=drink_id).thumb_img,
                'detail_img'        : Drink.objects.get(id=review.drink_id).drinkimage_set.get(drink_id=drink_id).detail_img,
                'drink_name'        : Drink.objects.get(id=review.drink_id).name,
                'drink_description' : Drink.objects.get(id=review.drink_id).description,
                'rating_averagy'    : Review.objects.filter(drink_id=drink_id).aggregate(Avg('rating')),
                'comment_count'     : Review.objects.filter(drink_id=drink_id).count(),
                'category'          : Drink.objects.get(id=review.drink_id).category.name,
                'caffeine'          : Drink.objects.get(id=review.drink_id).caffeine,
                'weight'            : Drink.objects.get(id=review.drink_id).weight,
                'price'             : Drink.objects.get(id=review.drink_id).price  
            } 
                for review in reviews if review.drink.id == drink_id
        ]
    
        return JsonResponse({'review':result}, status=200)
        