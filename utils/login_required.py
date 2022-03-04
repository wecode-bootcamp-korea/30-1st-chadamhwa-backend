import json, jwt

from django.contrib.auth.models import User
from django.http            import JsonResponse

from users.models           import User
from my_settings            import SECRET, ALGORITHM

def login_required(func): 
    def wrapper(self, request, *args, **kwargs):
        try: 
            token        = request.headers.get("Authorization", None)
            payload      = jwt.decode(token, SECRET, ALGORITHM)
            request.user = User.objects.get(id=payload['id'])

            return func(self, request, *args, **kwargs)

        except jwt.exceptions.DecodeError:                                     
            return JsonResponse({"message" : "INVALID_TOKEN" }, status=400)

        except User.DoesNotExist:
            return JsonResponse({"message" : "INVALID_USER"}, status=400)
            
    return wrapper
