from django.urls import path

from orders.views import CartView

urlpatterns = [
    path('/cart/drink<int:drink_id>/cart<int:cart_id>', CartView.as_view())
]