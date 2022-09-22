from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name 


class Account(models.Model):
    balance = models.DecimalField(max_digits=9, decimal_places=2)
    customer = models.ForeignKey(Customer, default=1, verbose_name= "customer_id", on_delete=models.SET_DEFAULT) 

    def __str__(self):
        return f"{self.customer} has {self.balance} in this account."


