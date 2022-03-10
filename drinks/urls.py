from django.urls import path

from drinks.views import ProductsView
from drinks.views import ProductDetailView

urlpatterns = [
    path('/products', ProductsView.as_view()),
    path('/details/<int:drink_id>', ProductDetailView.as_view())
]