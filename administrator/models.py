from django.contrib.auth.models import User
from django.db import models
from django.db import models
from decimal import Decimal

from django.utils import timezone


# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=50)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Brand(models.Model):
    name=models.CharField(max_length=50)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    Product_name=models.CharField(max_length=150)
    Brand=models.ForeignKey(Brand, on_delete=models.CASCADE)
    Category=models.ForeignKey(Category, on_delete=models.CASCADE)
    price=models.DecimalField(max_digits=8, decimal_places=2)
    Stock=models.DecimalField(max_digits=8, decimal_places=2)
    Description=models.CharField(max_length=200)
    img1=models.ImageField(upload_to='product_image')
    img2=models.ImageField(upload_to='product_image')
    img3=models.ImageField(upload_to='product_image')
    img4=models.ImageField(upload_to='product_image')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.Product_name

    def get_discounted_price(self):
        offers = Offer.objects.filter(product=self, start_date__lte=timezone.now(), end_date__gte=timezone.now())

        if offers.exists():
            offer = offers.first()

            if offer.discount_type == 'percentage':
                discount_amount = (offer.discount_value / Decimal(100)) * self.price
            else:
                discount_amount = offer.discount_value

            discounted_price = self.price - discount_amount
            return max(discounted_price, Decimal(0))  # Ensure discounted price is not negative
        else:
            return self.price

class Offer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount_type = models.CharField(max_length=10, choices=[('percentage', 'Percentage'), ('fixed', 'Fixed')])
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()


class Banner(models.Model):
    banner_name=models.CharField(max_length=50)
    img1=models.ImageField(upload_to='banner_image',null=True,blank=True)
    img2=models.ImageField(upload_to='banner_image',null=True,blank=True)
    img3=models.ImageField(upload_to='banner_image',null=True,blank=True)
    img4=models.ImageField(upload_to='banner_image',null=True,blank=True)
    img5=models.ImageField(upload_to='banner_image',null=True,blank=True)
    img6=models.ImageField(upload_to='banner_image',null=True,blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.banner_name
