# Generated by Django 3.2.15 on 2022-09-13 07:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=60)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('description', models.TextField()),
                ('publication_date', models.DateField()),
                ('image', models.ImageField(default='', upload_to='shop/images')),
                ('category', models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='shop.category')),
            ],
        ),
    ]
