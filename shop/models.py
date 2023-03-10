from django.db import models

# Create your models here.


class Product(models.Model):
    id = models.AutoField
    product_id = models.IntegerField(default=0)
    product_name = models.CharField(max_length=50, default="")
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=300, default="")
    pub_date = models.DateField()
    image = models.ImageField(upload_to="shop/images", default="")

    def __str__(self):
        return (self.product_name)


class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=70, default="")
    email = models.CharField(max_length=100, default="")
    desc = models.CharField(max_length=500, default="")
    phoneno = models.CharField(max_length=500, default="")

    def __str__(self):
        return (self.name)


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    # directly giving order to database...
    item_json = models.CharField(max_length=5000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=100, default="")


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)


def __str__(self):
    return self.update_desc[0:7] + "..."
