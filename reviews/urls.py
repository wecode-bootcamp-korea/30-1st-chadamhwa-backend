from django.urls import path

from reviews.views import CommentView

urlpatterns = [
    path('/comment', CommentView.as_view())
]