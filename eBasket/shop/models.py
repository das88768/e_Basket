from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=60)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=60)
    # category = models.CharField(max_length=60, default="")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=True, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    description = models.TextField()
    publication_date = models.DateField()
    image = models.ImageField(upload_to = "shop/images", default="")

    def __str__(self):
        return self.product_name