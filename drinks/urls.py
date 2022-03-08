from django.urls import path

from drinks.views import  ProductsView

urlpatterns = [
    path('/products', ProductsView.as_view()),
]