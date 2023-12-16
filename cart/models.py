from django.contrib.auth.models import User
from administrator.models import *
from django.db import models


# Create your models here.
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def _str_(self):
        return f"{self.user.username} - {self.product.Product_name}"

    def total_price(self):
        return self.product.get_discounted_price() * self.quantity