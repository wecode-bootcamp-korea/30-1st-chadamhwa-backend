from django.urls import path

from drinks.views import  ProductsView, FarmProductsView

urlpatterns = [
    path('/products', ProductsView.as_view()),
    path('/main', FarmProductsView.as_view())
]