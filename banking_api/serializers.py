
from rest_framework import serializers

from .models import Account, Customer


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'balance', 'customer']
