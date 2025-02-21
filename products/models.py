from django.db import models

class Category(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=100)
    price=models.DecimalField(decimal_places=2,max_digits=10)
    description=models.TextField()
    image_url=models.URLField()  
    created=models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category)
    available=models.BooleanField(default=True)
    available_units=models.IntegerField(default=0)
    number_of_units_added_to_carts=models.IntegerField(default=0)
    def __str__(self):
        return self.name
    



