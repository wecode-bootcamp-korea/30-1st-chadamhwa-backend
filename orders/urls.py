from django.urls import path

from orders.views import CartView

urlpatterns = [
    path('/carts/<int:cart_id>', CartView.as_view()),
    path('/carts', CartView.as_view())
]