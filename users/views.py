import json
import bcrypt
import jwt

from django.http  import JsonResponse
from django.views import View
from users.models import User
from my_settings  import SECRET, ALGORITHM

class SigninView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data['email']
            password = data['password']

            if not User.objects.filter(email=email).exists():
                return JsonResponse({'message':'INVALID_USER'}, status=400)

            user_password = User.objects.get(email=email).password

            if not bcrypt.checkpw(password.encode('utf-8'), user_password.encode('utf-8')):
                return JsonResponse({'message':'INVALID_USER'}, status=400)

            user = User.objects.get(email=email)
            payload = {'user_id':user.id}
            access_token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)

            return JsonResponse({'token': access_token}, status=200)

        except KeyError:
            return JsonResponse({'message':'Key_error'}, status=400)
            