# Generated by Django 3.2.15 on 2022-10-16 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_orderitem_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='country',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
