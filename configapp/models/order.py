from django.core.validators import RegexValidator
from django.db import models

from configapp.models import Product,User


class Order(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\+9989\d{8}$',
        message="Telefon raqam +9989XXXXXXXX formatida bo‘lishi kerak"
    )

    PENDING ='Pending'
    PROCESSING = 'processing'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELED =  'canceled'

    STATUS_CHOICES = [
        (PENDING,'Pending'),
        (PROCESSING,'processing'),
        (SHIPPED,'shipped'),
        (DELIVERED,'delivered'),
        (CANCELED,'canceled'),
    ]
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default=PENDING)
    phone_number = models.CharField(validators=[phone_regex],max_length=13,blank=True,null=True)

    def set_status(self,new_status):
        if new_status not in dict(self.STATUS_CHOICES):
            raise ValueError("Invalid Status")
        self.status = new_status
        self.save()

    def is_transition_allowed(self,new_status):
        allowed_transition = {
            self.PENDING:[self.PROCESSING,self.CANCELED],
            self.PROCESSING:[self.SHIPPED,self.CANCELED],
            self.SHIPPED:[self.DELIVERED,self.CANCELED]
        }
        return new_status in allowed_transition.get(self.status,[])
    def __str__(self):
        return f"{self.product.name} by {self.customer.email}"

