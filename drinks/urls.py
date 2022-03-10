from django.urls import path

from drinks.views import  ProductView, FarmProductView, ProductDetailView


urlpatterns = [
    path('/products', ProductView.as_view()),
    path('/farm-products', FarmProductView.as_view()),
    path('/details/<int:drink_id>', ProductDetailView.as_view())
]
