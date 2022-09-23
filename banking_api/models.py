from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name 


class Account(models.Model):
    balance = models.DecimalField(max_digits=9, decimal_places=2)
    customer_id = models.ForeignKey(Customer, default=1, verbose_name= "customer_id", on_delete=models.RESTRICT) 

    def __str__(self):
        return f"{self.customer_id} has {self.balance} in this account."

class Transfer(models.Model):
    date_time = models.DateTimeField(verbose_name='date_time', auto_now = True)
    sender_account_id = models.ForeignKey(Account, default=1, related_name='sender_account_id', on_delete=models.RESTRICT) 
    recipient_account_id = models.ForeignKey(Account, default=1, related_name='recipient_account_id', on_delete=models.RESTRICT) 
    amount = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return f"{self.sender_account_id.customer_id.name} (account #{self.sender_account_id.id}) transfered {self.amount}€ to \
            {self.recipient_account_id.customer_id.name} (account #{self.recipient_account_id.id}) on {self.date_time}."


