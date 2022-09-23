from decimal import Decimal

from django.db.models import Q
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Account, Customer, Transfer
from .serializers import (AccountSerializer, CustomerSerializer,
                          TransferSerializer)


@swagger_auto_schema(method='POST', request_body=AccountSerializer)
@api_view(['GET', 'POST'])
def account_list(request, format=None):

    if request.method == 'GET':
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return JsonResponse({'accounts': serializer.data}) 

    if request.method == 'POST':
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@swagger_auto_schema(method='POST', request_body=CustomerSerializer)
@api_view(['GET', 'POST'])
def customer_list(request, format=None):

    if request.method == 'GET':
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return JsonResponse({'customers': serializer.data}) 

    if request.method == 'POST':
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def account_balance(request, id, format=None):
    try:
        account = Account.objects.get(pk=id)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # data = request.GET.get()
    if request.method == 'GET':
        serializer = AccountSerializer(account)
        return Response(serializer.data['balance'])

@api_view(['GET'])
def account_transfers(request, id, format=None):
    try:
        account = Account.objects.get(pk=id)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        transfers = Transfer.objects.filter(Q(sender_id=id) | Q(recipient_id=id))
        serializer = TransferSerializer(transfers, many=True)
        return Response(serializer.data)

@swagger_auto_schema(method='POST', request_body=TransferSerializer)
@api_view(['GET', 'POST'])
def transfer_list(request, format=None):

    if request.method == 'GET':
        transfers = Transfer.objects.all()
        serializer = TransferSerializer(transfers, many=True)
        return JsonResponse({'transfers': serializer.data}) 

    if request.method == 'POST':
        # validate input data
        data=request.data
        try:
            sender_account_id = data['sender_account_id']
            recipient_account_id = data['recipient_account_id']
            amount = data['amount'] 
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            sender = Account.objects.get(pk=sender_account_id)
            recipient = Account.objects.get(pk=recipient_account_id)
        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # calculate new balances
        sender.balance = Decimal("{:.2f}".format(float(sender.balance) - float(amount)))
        recipient.balance = Decimal("{:.2f}".format(float(recipient.balance) + float(amount)))

        # update database
        sender_serializer = AccountSerializer(instance = sender, data={'balance':sender.balance})
        if sender_serializer.is_valid():
            sender_serializer.save()

        recipient_serializer = AccountSerializer(instance = recipient,data={'balance':recipient.balance})
        if recipient_serializer.is_valid():
            recipient_serializer.save()

        transfer_serializer = TransferSerializer(data=request.data)
        if transfer_serializer.is_valid():
            transfer_serializer.save()
            return Response(transfer_serializer.data, status=status.HTTP_201_CREATED) 
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
