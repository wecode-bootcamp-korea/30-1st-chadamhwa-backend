from django.db import models
from chadamhwa.time_stamp_model import TimeStampModel

class Drink(TimeStampModel):
    name     = models.CharField(max_length=45)
    price    = models.DecimalField(max_digits=10, decimal_places=2)
    caffeine = models.PositiveSmallIntegerField()
    weight   = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    farm     = models.ForeignKey('Farm', on_delete=models.CASCADE)
    image    = models.OneToOneField('DrinkImage', on_delete=models.CASCADE)

    class Meta:
        db_table = 'drinks'

class Category(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'categories'

class Farm(models.Model):
    name      = models.CharField(max_length=45)
    image_url = models.URLField(max_length=200)

    class Meta:
        db_table = 'farms'

class DrinkImage(models.Model):
    image_url = models.URLField(max_length=200)

    class Meta:
        db_table = 'drink_images'