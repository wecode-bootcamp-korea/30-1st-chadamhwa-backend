import json, bcrypt, jwt

from django.http  import JsonResponse
from django.views import View
from django.core.exceptions import ValidationError

from my_settings  import SECRET, ALGORITHM
from users.models import User
from users.utils  import login_required
from users.validation import validate_email, validate_password

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            username = data['username']
            email    = data['email'] 
            password = data['password']
            address  = data['address']
            point    = data.get('point', 100000)
            
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            validate_email(email)
            validate_password(password)

            if User.objects.filter(email = email).exists():
                return JsonResponse ({'message' : 'EMAIL_ALREADY_EXIST'}, status=400)

            if User.objects.filter(username = username).exists():
                return JsonResponse ({"message" : "USERNAME_ALREADY_EXIST"}, status=400)

            User.objects.create(
                username = username,
                email    = email,
                password = hashed_password,
                address  = address,
                point    = point         
            )

            return JsonResponse({'message' : 'SIGNUP_SUCCESS'}, status=201)

        except ValidationError as e:
            return JsonResponse({'message': e.message }, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)

        except KeyError:
            return JsonResponse ({'message' : 'KEY_ERROR'}, status=400)
 

class SignInView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            
            email    = data['email']
            password = data['password']

            if not User.objects.filter(email=email).exists():
                return JsonResponse({'message':'INVALID_USER'}, status=400)

            user_password = User.objects.get(email=email).password

            if not bcrypt.checkpw(password.encode('utf-8'), user_password.encode('utf-8')):
                return JsonResponse({'message':'INVALID_USER'}, status=400)

            user         = User.objects.get(email=email)
            payload      = {'id':user.id}
            access_token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)

            return JsonResponse({'message':'SUCCESS','token': access_token}, status=200)

        except KeyError:
            return JsonResponse({'message':'Key_error'}, status=400)
            