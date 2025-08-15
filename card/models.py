from django.db import models
from flowers_shop.settings import AUTH_USER_MODEL
from home.models import Flower
# Create your models here.

User = AUTH_USER_MODEL

class Card(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())


class CardItem(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='items')
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE, blank=True, null=True)
    ammount = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.flower.name

    @property
    def total_price(self):
        return self.flower.price * self.ammount