from django.db     import models

class User(models.Model):
    username   = models.CharField(max_length=10, unique=True)
    email      = models.CharField(max_length=100, unique=True)
    password   = models.CharField(max_length=256)
    address    = models.CharField(max_length=256)
    point      = models.PositiveIntegerField(default=100000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

class Review(models.Model):
    user       = models.ForeignKey('User', on_delete=models.CASCADE)
    drink      = models.ForeignKey('drinks.Drink', on_delete=models.CASCADE)
    rating     = models.PositiveSmallIntegerField()
    comment    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    class Meta:
        db_table = 'reviews'