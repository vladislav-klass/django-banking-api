
from rest_framework import serializers

from .models import Account, Customer, Transfer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name']

class AccountSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.balance = validated_data.get('balance', instance.balance)
        instance.save()
        return instance    

    class Meta:
        model = Account
        fields = ['id', 'balance', 'customer_id']

class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ['id', 'date_time', "sender_id", "recipient_id", "amount"]
