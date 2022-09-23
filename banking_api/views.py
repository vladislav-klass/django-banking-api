from decimal import Decimal

from django.db.models import Q
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Account, Customer, Transfer
from .serializers import (AccountSerializer, CustomerSerializer,
                          TransferSerializer)


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
            sender_id = data['sender_id']
            recipient_id = data['recipient_id']
            amount = data['amount'] 
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            sender = Account.objects.get(pk=sender_id)
            recipient = Account.objects.get(pk=recipient_id)
        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # calculate new balances
        sender.balance = Decimal("{:.2f}".format(float(sender.balance) - amount))
        recipient.balance = Decimal("{:.2f}".format(float(recipient.balance) + amount))

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
