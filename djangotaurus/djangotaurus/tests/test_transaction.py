from django.test import TestCase, Client
from ..models import User, Profile, Transaction, Stock, StockPriceCurrent
from django.urls import reverse
from datetime import datetime


class Test_Transaction(TestCase):
    """
    Things to test:
        - Purchasing stock where user has enough balance -> Done
        - Purchasing stock where user does not have enough money to fulfill -> Done
        - Purchasing stock where user enters a negative value in quantity -> Done
        - Selling partial lot quantity of holding stock -> Done
        - Selling all lot quantity of the stock purchased in the transaction -> Done
        - Trying to sell more lot quantity then actual holding -> Done
        - Purchasing stock where user enters a negative value in quantity -> Done
    """

    def setUp(self):
        super().setUp()
        self.client = Client()

        # Set up Teacher Account
        self.teacher = User.objects.create(email='teacher123@gmail.com', is_staff=True)
        self.teacher.set_password(
            "5e665efdd3a76a7c05e2f0955e290c6f7fc80306642cb131e175c019cea86ffecc73fa1f1e5b191e287ffce7211d545e41467da49f015c1074d2951fc13567091b5ce834fb23e45a60ea0b9ba3a4eec05c45f3633e840e9b707bfc82be8189b78665bb0d96bc18c80f676cff648df2142440986307a744a778c016e449e5a1830192ba24808eede0e9c9e054c3c9b9f5356e4f10ca1b84164abbcd931ef8fbaab1f90ecb78ea9e6a46f054e251361babea01286dda37b806165ccd24abbf97f69b798d9316499a6fb0abf98ebf3ec0a05f6a7ae1b70cbb26855e05705cd5e0c2403a799b0f8e69020c93e1d3ffadb55ebcb7e8db7b961b44dd46066c117a00c8",
            "4cefde6e2dc65670be52b4f224a07566ec7303254d31fa85d3b6bc34ccea6932")
        self.teacher.save()

        self.teacherProfile = Profile(first_name="John", last_name="Smith", owner=self.teacher,
                                      date_of_birth=datetime.strptime("24/12/1996", "%d/%m/%Y"))
        self.teacherProfile.save()

        # Set up Student Account
        self.student = User.objects.create(email='student123@gmail.com')
        self.student.set_password(
            "5e665efdd3a767ac05e2f0955e290c6f7fc80306642cb131e175c019cea86ffecc73fa1f1e5b191e287ffce7211d545e41467da49f015c1074d2951fc13567091b5ce834fb23e45a60ea0b9ba3a4eec05c45f3633e840e9b707bfc82be8189b78665bb0d96bc18c80f676cff648df2142440986307a744a778c016e449e5a1830192ba24808eede0e9c9e054c3c9b9f5356e4f10ca1b84164abbcd931ef8fbaab1f90ecb78ea9e6a46f054e251361babea01286dda37b806165ccd24abbf97f69b798d9316499a6fb0abf98ebf3ec0a05f6a7ae1b70cbb26855e05705cd5e0c2403a799b0f8e69020c93e1d3ffadb55ebcb7e8db7b961b44dd46066c117a00c8",
            "4cefde6e2dc65670eb52b4f224a07566ec7303254d31fa85d3b6bc34ccea6932")
        self.student.save()

        self.studentProfile = Profile(first_name="Crazy", last_name="Joe", owner=self.student,
                                      date_of_birth=datetime.strptime("20/11/1998", "%d/%m/%Y"))
        self.studentProfile.save()

        # Set up one Stock
        self.stock = Stock(company_name="TESLA", company_desc="This is a test",
                           image_url="https://imgur.com/gallery/KT1kwRV",
                           stock_symbol="TSLA", sector="Transport", industry="Transport")
        self.stock.save()
        self.stock_price = StockPriceCurrent(high=0.012, low=0.012, open=0.012, close=0.012, stock=self.stock)
        self.stock_price.save()

    def test_purchase_stock_with_enough_balance(self):
        """
            Purchasing stock where user has enough balance

            Stock will be purchase and an active transaction will be created. The amount used to purchase the stock will
            be deducted from user account balance.
        """
        self.client.force_login(self.student)
        response = self.client.post(reverse('buyStock'), {'stock_id': self.stock.id, 'option': "BUY", 'quantity': 1000})

        transaction = Transaction.objects.filter(owner=self.student).first()
        user = User.objects.get(email=self.student.email)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Transaction.objects.filter(owner=self.student).exists())
        self.assertEqual("TSLA", str(transaction.stock.stock_symbol))
        self.assertEqual(True, transaction.active)
        self.assertNotEqual(1000.0, user.profile.account_balance)

    def test_purchase_stock_with_not_enough_balance(self):
        """
            Purchasing stock where user does not have enough money to fulfill

            Stock will be not be purchased, no active transaction will be created
        """
        self.client.force_login(self.student)
        response = self.client.post(reverse('buyStock'),
                                    {'stock_id': self.stock.id, 'option': "BUY", 'quantity': 1000000000})

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Transaction.objects.filter(owner=self.student).exists())

    def test_purchase_stock_with_a_negative_quantity(self):
        """
            Purchasing stock where user enters a negative value in quantity

            Stock will be not be purchased, no active transaction will be created
        """
        self.client.force_login(self.student)
        response = self.client.post(reverse('buyStock'),
                                    {'stock_id': self.stock.id, 'option': "BUY", 'quantity': -1})

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Transaction.objects.filter(owner=self.student).exists())

    def test_sell_stock_with_leftover_quantity(self):
        """
            Selling partial lot quantity of holding stock.

            Stock will be sold, active transaction will remain, deducting the amount of lot sold and create a
            sell transaction for the amount of lot sold.
        """
        self.client.force_login(self.student)
        self.client.post(reverse('buyStock'), {'stock_id': self.stock.id, 'option': "BUY", 'quantity': 100})
        sell_response = self.client.post(reverse('sellStock'),
                                         {'stock_id': self.stock.id, 'option': "BUY", 'buyOpt': 50})

        transaction = Transaction.objects.filter(owner=self.student, stock=self.stock, active=True).first()

        self.assertEqual(sell_response.status_code, 302)
        self.assertEqual(50, transaction.lot_quantity)
        self.assertEqual(True, transaction.active)

    def test_sell_stock_all_quantity(self):
        """
            Selling all lot quantity of the stock purchased in the transaction.

            Stock will be sold, active transaction will remain, lot quantity will be 0.
        """
        self.client.force_login(self.student)
        self.client.post(reverse('buyStock'), {'stock_id': self.stock.id, 'option': "BUY", 'quantity': 100})

        sell_response = self.client.post(reverse('sellStock'),
                                         {'stock_id': self.stock.id, 'option': "BUY", 'buyOpt': 100})

        transaction = Transaction.objects.filter(owner=self.student, stock=self.stock, active=True).first()

        self.assertEqual(sell_response.status_code, 302)
        self.assertEqual(0, transaction.lot_quantity)
        self.assertEqual(True, transaction.active)

    def test_sell_more_stock_then_holding_quantity(self):
        """
            Trying to sell more lot quantity then actual holding

            Stock will not be sold and a error message will be post back to user.
        """
        self.client.force_login(self.student)
        self.client.post(reverse('buyStock'), {'stock_id': self.stock.id, 'option': "BUY", 'quantity': 100})
        sell_response = self.client.post(reverse('sellStock'),
                                         {'stock_id': self.stock.id, 'option': "BUY", 'buyOpt': 150})

        transaction = Transaction.objects.get(owner=self.student, stock=self.stock, active=True)

        self.assertEqual(sell_response.status_code, 302)
        self.assertEqual(100, transaction.lot_quantity)
        self.assertEqual(True, transaction.active)

    def test_sell_stock_with_a_negative_quantity(self):
        """
            Purchasing stock where user enters a negative value in quantity

            Stock will be not be purchased, no active transaction will be created
        """
        self.client.force_login(self.student)
        self.client.post(reverse('buyStock'), {'stock_id': self.stock.id, 'option': "BUY", 'quantity': 100})
        sell_response = self.client.post(reverse('sellStock'),
                                         {'stock_id': self.stock.id, 'option': "BUY", 'buyOpt': -1})

        transaction = Transaction.objects.get(owner=self.student, stock=self.stock, active=True)

        self.assertEqual(sell_response.status_code, 302)
        self.assertEqual(100, transaction.lot_quantity)
        self.assertEqual(True, transaction.active)
