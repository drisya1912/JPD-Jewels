# Generated by Django 5.0 on 2023-12-10 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='user',
        ),
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
        migrations.RemoveField(
            model_name='applied_coupon',
            name='user',
        ),
        migrations.DeleteModel(
            name='Banner',
        ),
        migrations.RemoveField(
            model_name='product',
            name='Brand',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='product',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='user',
        ),
        migrations.RemoveField(
            model_name='product',
            name='Category',
        ),
        migrations.DeleteModel(
            name='Coupon',
        ),
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.RemoveField(
            model_name='wallet',
            name='order',
        ),
        migrations.RemoveField(
            model_name='returnedproduct',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='product',
        ),
        migrations.RemoveField(
            model_name='wishitem',
            name='product',
        ),
        migrations.RemoveField(
            model_name='user_profile',
            name='user',
        ),
        migrations.RemoveField(
            model_name='wallet',
            name='user',
        ),
        migrations.RemoveField(
            model_name='wishitem',
            name='user',
        ),
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.DeleteModel(
            name='Applied_coupon',
        ),
        migrations.DeleteModel(
            name='Brand',
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='ReturnedProduct',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.DeleteModel(
            name='User_profile',
        ),
        migrations.DeleteModel(
            name='Wallet',
        ),
        migrations.DeleteModel(
            name='WishItem',
        ),
    ]
