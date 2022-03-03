import json, jwt, re

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http            import JsonResponse

from users.models           import User
from my_settings            import SECRET, ALGORITHM

def login_decorator(func): 
    def wrapper(self, request, *args, **kwargs):
        try: 
            token        = request.headers.get("Authorization", None)
            payload      = jwt.decode(token, SECRET, ALGORITHM)
            request.user = User.objects.get(id=payload['user_id'])

            return func(self, request, *args, **kwargs)

        except jwt.exceptions.DecodeError:                                     
            return JsonResponse({"message" : "INVALID_TOKEN" }, status=400)

        except ObjectDoesNotExist:
            return JsonResponse({"message" : "INVALID_USER"}, status=400)
            
    return wrapper

def email_validation(email):
    EMAIL_REGEX = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9.]+$'
    
    if not re.match(EMAIL_REGEX, email):
          raise ValidationError('INVALID_EMAIL')

def password_validation(password):
    PASSWORD_REGEX = PASSWORD_REGEX = '^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'
    
    if not re.match(PASSWORD_REGEX, password):
          raise ValidationError('INVALID_PASSWORD')