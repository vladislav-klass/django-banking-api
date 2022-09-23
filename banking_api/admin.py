from django.contrib import admin

from .models import Account, Customer, Transfer

admin.site.register(Account)
admin.site.register(Customer)
admin.site.register(Transfer)



