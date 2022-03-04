import json

from django.views import View
from django.http  import JsonResponse

class PostingView(View):
    def post(self, request):

        try:
            data = json.loads(request.body)
