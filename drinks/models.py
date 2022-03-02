from django.db import models

class Drink(models.Model):
    name       = models.CharField(max_length=45)
    price      = models.DecimalField(max_digits=10, decimal_places=2)
    caffeine   = models.PositiveSmallIntegerField()
    weight     = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category   = models.ForeignKey('Category', on_delete=models.CASCADE)
    farm       = models.ForeignKey('Farm', on_delete=models.CASCADE)
    image      = models.OneToOneField('Image', on_delete=models.CASCADE)

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

class Image(models.Model):
    image_url = models.URLField(max_length=200)

    class Meta:
        db_table = 'images'