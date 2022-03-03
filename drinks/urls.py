from django.urls import path

from drinks.views import  FilteringView

urlpatterns = [
    path('/filtering', FilteringView.as_view()),
]