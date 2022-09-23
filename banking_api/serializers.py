
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
        fields = ['id', 'date_time', "sender_account_id", "recipient_account_id", "amount"]


# class ProjectView(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):

#     permission_classes = [permissions.IsAuthenticated, ] 
#     serializer_class = ProjectSerializer
#     queryset = Project.objects.all()

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)