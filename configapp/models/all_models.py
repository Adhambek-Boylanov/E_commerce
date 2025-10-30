from datetime import timezone

from django.db import models

from .auth_user import User
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def is_in_stock(self):
        return self.stock>0

    def reduce_stock(self,quantity):
        if quantity > self.stock:
            return False
        self.stock-= quantity
        self.save()

    def increase_stock(self,amount):
        self.stock += amount
        self.save()


class Review(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="reviews")
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="reviews")
    content = models.TextField()
    rating = models.PositiveIntegerField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.rating}"
class FlashSale(models.Model):
    product = models.OneToOneField(Product,on_delete=models.CASCADE)
    discount_percentage = models.PositiveIntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def is_active(self):
        now = timezone.now()
        return self.start_time <= now <= self.end_time
    class Meta:
        unique_together = ('product','start_time','end_time')
    def __str__(self):
        return f"{self.product} --> {self.discount_percentage}"
class ProductViewHistory(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    timestap = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"


