from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User



class Car(models.Model):
    car_id = models.IntegerField(primary_key=True, max_length=10, db_index=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    year = models.PositiveIntegerField ()
    price = models.PositiveIntegerField()
    km_driven = models.PositiveBigIntegerField()
    mileage = models.DecimalField(max_digits=4, decimal_places=2)
    engine = models.PositiveIntegerField ()
    transmission = models.CharField (max_length=20)
    fuel_type = models.CharField (max_length=20)
    seller_type = models.CharField (max_length=20)
    owner = models.CharField (max_length=100)
    seats = models.PositiveSmallIntegerField()
    running_cost = models.CharField (max_length=20)
    image = models.ImageField (upload_to = 'carimages/')
    slug = models.SlugField(max_length=255)
    
    class Meta:
        verbose_name_plural = 'Cars'
    
    def __str__(self):
        return self.name

class Wants(models.Model):
    buyer = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    wanted_car_id = models.ForeignKey(Car, related_name='wanted', default=None, null=True, on_delete=models.CASCADE)
    recommended_car_id = models.ForeignKey(Car, related_name='recommended', default=None, null=True, on_delete=models.CASCADE)
    year = models.PositiveIntegerField ()
    price = models.PositiveIntegerField()
    km_driven = models.PositiveBigIntegerField()
    mileage = models.DecimalField(max_digits=4, decimal_places=2)
    engine = models.PositiveIntegerField ()
    transmission = models.CharField (max_length=20)
    fuel_type = models.CharField (max_length=20)
    seller_type = models.CharField (max_length=20)
    owner = models.CharField (max_length=100)
    seats = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name_plural = 'Wants'

    def __str__(self):
        return self.buyer.username

class Recommendations(models.Model):
    buyer = models.ForeignKey(User, related_name='buyer',default=None, on_delete=models.CASCADE)
    car_id = models.IntegerField(max_length=10, db_index=True)
    seller = models.ForeignKey(User, related_name='seller',on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    year = models.PositiveIntegerField ()
    price = models.PositiveIntegerField()
    km_driven = models.PositiveBigIntegerField()
    mileage = models.DecimalField(max_digits=4, decimal_places=2)
    engine = models.PositiveIntegerField ()
    transmission = models.CharField (max_length=20)
    fuel_type = models.CharField (max_length=20)
    seller_type = models.CharField (max_length=20)
    owner = models.CharField (max_length=100)
    seats = models.PositiveSmallIntegerField()
    running_cost = models.CharField (max_length=20)
    image = models.ImageField (upload_to = 'carimages/')
    score = models.DecimalField(max_digits=6, decimal_places=3)
    
    class Meta:
        verbose_name_plural = 'Recommendations'
    
    def __str__(self):
        return self.buyer.username

class RecommendationFeedback(models.Model):
    id = models.IntegerField(primary_key=True, max_length=10, db_index=True)
    year = models.DecimalField(max_digits=9, decimal_places=5)
    price = models.DecimalField(max_digits=9, decimal_places=5)
    km_driven = models.DecimalField(max_digits=9, decimal_places=5)
    mileage = models.DecimalField(max_digits=9, decimal_places=5)
    engine = models.DecimalField(max_digits=9, decimal_places=5)
    
    class Meta:
        verbose_name_plural = 'RecommendationsFeedback'
    
    def __str__(self):
        return str(self.id)

class Page(models.Model):
    name = models.CharField(max_length=255)
    page_link = models.URLField(max_length=200)

    class Meta:
        verbose_name_plural = 'Pages'
    
    def __str__(self):
        return self.name