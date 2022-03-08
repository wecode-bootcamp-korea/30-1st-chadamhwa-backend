from django.urls import path

from reviews.views import CommentView

urlpatterns = [
    path('/comments/<int:drink_id>', CommentView.as_view())
]