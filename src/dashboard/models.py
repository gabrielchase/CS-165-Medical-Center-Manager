from django.db import models


class Service(models.Model):

    name = models.CharField(max_length=255, primary_key=True)
    # description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    
    product_id = models.AutoField(primary_key=True)
    generic_name = models.CharField(max_length=255, null=False)
    brand_name = models.CharField(max_length=255, null=False)
    manufacturer = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.generic_name
