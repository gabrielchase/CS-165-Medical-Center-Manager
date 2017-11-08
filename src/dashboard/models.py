from django.db import models


class Service(models.Model):

    name = models.CharField(max_length=255, primary_key=True)
    # description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    
    product_id = models.AutoField(primary_key=True)
    generic_name = models.CharField(max_length=255)
    brand_name = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.generic_name
