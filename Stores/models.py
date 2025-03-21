from django.db import models

# Create your models here.

class Store(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=30, decimal_places=20)
    longitude = models.DecimalField(max_digits=30, decimal_places=20)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    image_url=models.URLField()  
    rating = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    
    def __str__(self):
        return self.name