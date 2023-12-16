import uuid
from django.contrib.auth.models import User
from django.db import models
from administrator.models import Product
from user_account.models import Address


# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='order_user', null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    billing_status = models.CharField(max_length=10, )
    paid = models.BooleanField(default=False)
    discount = models.IntegerField(blank=True, null=True, default=0)

    RETURNED = 'Returned'
    CANCEL = 'Cancelled'
    ORDER_STATUS_CHOICES = [
        ('confirmed', 'Order Confirmed'),
        ('shipped', 'Shipped'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        (CANCEL, 'Cancelled'),
        (RETURNED, 'Returned')
    ]
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='confirmed')

    class Meta:
        ordering = ('-created',)

    def _str_(self):
        return f"{self.created} - {self.status}"

    @classmethod
    def get_user_order_status(cls, user):
        latest_order = cls.objects.filter(user=user).order_by('-created').first()
        if latest_order:
            return latest_order.status
        return None


class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name='order_items',on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name='order_items',on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def _str_(self):
        return str(self.id)


class ReturnedProduct(models.Model):
    RETURN_PENDING = 'Return Pending'
    RETURNED = 'Returned'
    REJECTED = 'Rejected'

    RETURN_STATUS_CHOICES = (
        (RETURN_PENDING, 'Return Pending'),
        (RETURNED, 'Returned'),
        (REJECTED, 'Rejected')
    )

    order = models.ForeignKey(Order, related_name='returned_products', on_delete=models.CASCADE)
    reason = models.TextField()
    return_status = models.CharField(max_length=20, choices=RETURN_STATUS_CHOICES, default=RETURN_PENDING)
    returned_at = models.DateTimeField(auto_now_add=True)
    received_at = models.DateTimeField(null=True, blank=True)

    def _str_(self):
        return f"{self.order.id} - {self.return_status}"


class Wallet(models.Model):
    DEBIT = 'Debit'
    CREDIT = 'Credit'

    BALANCE_TYPE = (
        (DEBIT, 'Debit'),
        (CREDIT, 'Credit')
    )
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.IntegerField(default=0)
    balance_type = models.CharField(max_length=15, choices=BALANCE_TYPE, default=CREDIT)
    balance_returned = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.user.username}'s Wallet"

    def total_balance(self):
        balance = 0
        if self.balance_type == Wallet.DEBIT:
            balance -= self.amount
        else:
            balance += self.amount
        return balance



