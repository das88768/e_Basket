# Generated by Django 3.2.15 on 2023-05-15 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_customer_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image2',
            field=models.ImageField(default='', upload_to='shop/images'),
        ),
    ]
