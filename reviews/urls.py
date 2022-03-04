from django.urls import path

from reviews.views import PostingView

urlpatterns = [
    path('posting', PostingView.as_view())
]