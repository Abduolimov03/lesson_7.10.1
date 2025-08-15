from django.db import models
from home.models import Flower
from user_acc.models import CustomUser
# Create your models here.


class Order(models.Model):
    STATUS_CHOISE = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('canceled','canceled' )
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOISE, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.status

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, blank=True, null=True)
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)
    ammount = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.flower.name

    @property
    def total_price(self):
        return self.flower.price * self.ammount