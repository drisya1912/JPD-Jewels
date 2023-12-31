# Generated by Django 5.0 on 2023-12-10 18:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner_name', models.CharField(max_length=50)),
                ('img1', models.ImageField(blank=True, null=True, upload_to='banner_image')),
                ('img2', models.ImageField(blank=True, null=True, upload_to='banner_image')),
                ('img3', models.ImageField(blank=True, null=True, upload_to='banner_image')),
                ('img4', models.ImageField(blank=True, null=True, upload_to='banner_image')),
                ('img5', models.ImageField(blank=True, null=True, upload_to='banner_image')),
                ('img6', models.ImageField(blank=True, null=True, upload_to='banner_image')),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Product_name', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('Stock', models.DecimalField(decimal_places=2, max_digits=8)),
                ('Description', models.CharField(max_length=200)),
                ('img1', models.ImageField(upload_to='product_image')),
                ('img2', models.ImageField(upload_to='product_image')),
                ('img3', models.ImageField(upload_to='product_image')),
                ('img4', models.ImageField(upload_to='product_image')),
                ('active', models.BooleanField(default=True)),
                ('Brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.brand')),
                ('Category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.category')),
            ],
        ),
    ]
