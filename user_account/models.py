from django.contrib.auth.models import User
from django.db import models
from administrator.models import Product

# Create your models here.
class User_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    profile_photo = models.ImageField(upload_to="profile_photos/")
    phone_number = models.CharField( max_length=13, )
    address = models.CharField(max_length=100)

class WishItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    address = models.TextField()
    place = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f'{self.full_name} - {self.address}, {self.place}, {self.pincode}'


class Applied_coupon(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    coupon = models.CharField(max_length=50, null=True, blank=True)

