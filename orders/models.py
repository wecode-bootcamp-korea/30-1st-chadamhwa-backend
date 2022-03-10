from django.db import models

from utils import TimeStampModel

class Order(TimeStampModel):
    user   = models.ForeignKey('users.User', on_delete=models.CASCADE)
    status = models.ForeignKey('OrderStatus', on_delete=models.CASCADE)

    class Meta:
        db_table = 'orders'

class OrderStatus(models.Model):
    status = models.CharField(max_length=45)

    class Meta:
        db_table = 'order_statuses'

class OrderItem(models.Model):
    quantity     = models.PositiveSmallIntegerField(default=1)
    price        = models.DecimalField(max_digits=10, decimal_places=2)
    order_number = models.CharField(max_length=200)
    drink        = models.ForeignKey('drinks.Drink', on_delete=models.CASCADE)
    order        = models.ForeignKey('Order', on_delete=models.CASCADE)

    class Meta:
        db_table = 'order_items'

class Cart(TimeStampModel):
    quantity = models.PositiveSmallIntegerField()
    drink    = models.ForeignKey('drinks.Drink', on_delete=models.CASCADE)
    user     = models.ForeignKey('users.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'carts'
    

