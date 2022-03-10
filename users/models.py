from django.db     import models

from utils.time_stamp_model import TimeStampModel

class User(TimeStampModel):
    username = models.CharField(max_length=10, unique=True)
    email    = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=256)
    address  = models.CharField(max_length=256)
    point    = models.PositiveIntegerField(default=100000)

    class Meta:
        db_table = 'users'

class Review(TimeStampModel):
    user    = models.ForeignKey('User', on_delete=models.CASCADE)
    drink   = models.ForeignKey('drinks.Drink', on_delete=models.CASCADE)
    rating  = models.PositiveSmallIntegerField()
    comment = models.TextField() 

    class Meta:
        db_table = 'reviews'