from django.urls import path

<<<<<<< HEAD
from drinks.views import ProductView
from drinks.views import ProductDetailView

urlpatterns = [
    path('/products', ProductView.as_view()),
    path('/details/<int:drink_id>', ProductDetailView.as_view())
]
=======
from drinks.views import  ProductView, FarmProductView

urlpatterns = [
    path('/products', ProductView.as_view()),
    path('/farm-products', FarmProductView.as_view())
>>>>>>> c00f0a085a7caef66738503bfdc54894aa40c2ed
]