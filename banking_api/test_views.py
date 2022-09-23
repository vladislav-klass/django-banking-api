from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import (APIRequestFactory, APITestCase,
                                 force_authenticate)

from .models import Account, Customer, Transfer
from .views import (account_balance, account_list, account_transfers,
                    customer_list, transfer_list)


class BankAPIViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        Ben = Customer.objects.create(name='Ben')
        Larry = Customer.objects.create(name='Larry')

        Account.objects.create(balance='100', customer_id = Ben)
        Account.objects.create(balance='200', customer_id = Ben)
        Account.objects.create(balance='3000', customer_id = Larry)        

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/accounts/')
        self.assertEqual(response.status_code, 200)

    # TODO: Test all models and views

    def setUp(self):
        pass

