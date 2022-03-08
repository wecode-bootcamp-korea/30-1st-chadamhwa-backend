from django.urls import path

from orders.views import CartView

urlpatterns = [
    path('/cart/drink-id=<int:drink_id>/cart-id=<int:cart_id>', CartView.as_view())
]