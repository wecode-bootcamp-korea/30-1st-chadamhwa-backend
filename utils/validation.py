import re

from django.core.exceptions import ValidationError

def validate_email(email):
    EMAIL_REGEX = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9.]+$'
    
    if not re.match(EMAIL_REGEX, email):
          raise ValidationError('INVALID_EMAIL')

def validate_password(password):
    PASSWORD_REGEX = PASSWORD_REGEX = '^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'
    
    if not re.match(PASSWORD_REGEX, password):
          raise ValidationError('INVALID_PASSWORD')
          