from django.urls import path

from drinks.views import  ProductsView, FarmProductsView

urlpatterns = [
    path('/products', ProductsView.as_view()),
    path('/farm-products', FarmProductsView.as_view())
]