from django.urls import path

from drinks.views import  ProductView, FarmProductView

urlpatterns = [
    path('/products', ProductView.as_view()),
    path('/farm-products', FarmProductView.as_view())
]