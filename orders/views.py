import json, jwt

from django.http  import JsonResponse
from django.views import View

from orders.models import Cart
from drinks.models import Drink
from utils.login_required import login_required

class CartView(View):
    @login_required
    def get(self, request):

        carts  = Cart.objects.select_related('drink').filter(user = request.user)

        result = [
            {
            'cart_id'    : cart.id,
            'drink_name' : cart.drink.name,
            'quantity'   : cart.quantity,
            'price'      : cart.drink.price
            }
            for cart in carts]

        return JsonResponse({'result' : result}, status = 200)

    @login_required
    def post(self, request, drink_id):
        try:
            data = json.loads(request.body)
            
            user     = request.user
            quantity = data['quantity']

            if not Drink.objects.filter(id = drink_id).exists():
                return JsonResponse({'message' : 'DRINK_NOT_EXIST'}, status = 400)

            cart, created = Cart.objects.get_or_create(
                user     = user,
                drink_id = drink_id,
                quantity = quantity
            )

            cart.save()

            return JsonResponse({'message' : 'CART_CREATED'}, status = 201)

        except json.JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status = 400)  

        except Cart.DoesNotExist:
            return JsonResponse({'message' : 'CART_NOT_FOUND'}, status = 400)  
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

    @login_required
    def patch(self, request):
        try:
            data = json.loads(request.body)

            cart          = Cart.objects.get(id = data['cart_id'])
            cart.quantity = data['quantity']
            
            cart.save()
            
            return JsonResponse({'quantity' : cart.quantity}, status = 200)

        except Cart.DoesNotExist:
            return JsonResponse({'message' : 'CART_NOT_FOUND'}, status = 400)  

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

    @login_required
    def delete(self, request, cart_id):
        try:
            data = json.loads(request.body)

            user = request.user

            if not Cart.objects.filter(user = user, id = cart_id).exists():
                return JsonResponse({'message' : 'CART_DOES_NOT_EXIST'}, status = 400)

            Cart.objects.filter(user = user, id = cart_id).delete()

            return JsonResponse({'message' : 'CART_DELETED'}, status = 204)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)


class OrderView(View):
	def post(self, request):
		user = request.user

		# quantity
		# price
		# order_number
		# drink
		# order
