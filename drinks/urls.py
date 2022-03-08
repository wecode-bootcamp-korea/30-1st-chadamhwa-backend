from django.urls import path

from drinks.views import  ProductsView, MainView

urlpatterns = [
    path('/products', ProductsView.as_view()),
    path('/main', MainView.as_view())
]