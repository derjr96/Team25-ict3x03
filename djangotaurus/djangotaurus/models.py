import email as Email
import secrets
import string
import smtplib
import ssl
from datetime import datetime, timezone
from typing import List
from uuid import uuid4
import requests

import yfinance as yf
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.sessions.models import Session
from django.db import models
from django.conf import settings

from .validation import Validation, Validation_Functions



class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)
    password = models.CharField(max_length=512)
    account_lock = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    salt = models.CharField(max_length=64, unique=True, null=True)
    last_pw_change = models.DateTimeField(null=True)
    last_pw_reset = models.DateTimeField(null=True)
    last_login_attempt = models.DateTimeField(null=True)
    login_attempts = models.IntegerField(default=0)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def delete_user(self):
        self.delete()

    def get_invested_amount(self):
        transactions = Transaction.objects.get_user_transactions(self)
        invested = 0.0
        for transaction in transactions:
            invested += float(transaction.price) * transaction.lot_quantity
        return round(invested, 3)

    def get_total_amount(self):
        return round(self.get_invested_amount() + float(self.profile.account_balance), 3)

    def set_verified(self, verified=True):
        self.verified = verified
        self.save()

    def get_invested_industry(self) -> List[list]:
        industry_invested = []
        active_transaction = Transaction.objects.get_active_transactions(self)

        for investment in active_transaction:
            if investment.lot_quantity > 0:
                not_exist = False
                stock_industry = Transaction.get_stock_industry(investment)
                invested = float(investment.price) * investment.lot_quantity
                if len(industry_invested) == 0:
                    temp_list = [stock_industry, invested]
                    industry_invested.append(temp_list)
                else:
                    for industry in industry_invested:
                        if industry[0] == stock_industry:
                            industry[1] += invested
                            break
                        else:
                            not_exist = True

                if not_exist:
                    temp_list = [stock_industry, invested]
                    industry_invested.append(temp_list)

        return industry_invested

    def set_password(self, password, salt):
        if Validation_Functions.validate_new_password(password, salt):
            self.password = password
            self.salt = salt
            self.save()
        else:
            raise ValueError("Password validation failed")

    def lock_account(self, lock=True):
        self.account_lock = lock
        self.save()

    def set_login_attempt(self):
        self.login_attempts += 1
        self.last_login_attempt = datetime.now(timezone.utc)
        self.save()

    def reset_login_attempts(self):
        self.login_attempts = 0
        self.save()
    
    def remove_all_sessions(self):
        user_sessions = []
        for session in Session.objects.all():
            if str(self.pk) == session.get_decoded().get('_auth_user_id'):
                user_sessions.append(session.pk)
        return Session.objects.filter(pk__in=user_sessions).delete()

    def __str__(self):
        return self.email


class Profile(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    date_of_birth = models.DateField()
    account_balance = models.DecimalField(max_digits=8, decimal_places=3, default=1000.00)
    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.date_of_birth} {self.account_balance}'

    def reset_profile(self):
        """
            Function to reset the user's profile entirely, by clearing all current and past transactions related to the
            user and return account balance to the original starting amount of $1000.00.

            @params:
                self, the profile model object
        """
        self.account_balance = 1000.00
        Transaction.objects.delete_user_transactions(self.owner)
        self.save()

    def update_profile(self, fn, ln) -> bool:
        """
            Function to update the user profile first name and last name

            @params:
                self, the profile model object
                fn, new first name
                ln, new last name
            @returns: bool, True if param inputs are valid
        """
        if Validation_Functions.validate_profile_update(fn, ln):
            self.first_name = fn
            self.last_name = ln
            self.save()
            return True
        else:
            return False

    def modify_balance(self, amount) -> bool:
        """
            Function to deposit virtual credits into the student's account

            @params:
                self, the profile model object
                amount, a float value to add to the student's balance
            @returns: bool, True if amount input is valid, 0 < amount < 501
        """
        amount = float(amount)
        if Validation_Functions.validate_deposit(amount):
            self.account_balance = round(float(self.account_balance) + amount, 3)
            self.save()
            return True
        else:
            return False


class AccessTokenManager(models.Manager):
    """
        Accesses Access Token Model

        class functions available:
            - generate_token(self, user, type, lifespan)
            - verify_token(self, token_str)
            - expire_token(self, uuid)
            - expire_old_token(self, user, access_type)
    """

    def generate_token(self, user, type, lifespan):
        """
            Function to generate an access token based on the type entered and send an email to the user

            @params:
                self, the access token model object
                user, user object
                type, type of token to generate (OTP, RESETPW, VERIFY)
                lifespan, the life span of the token for validating if its' valid
        """

        if type == 'OTP':
            generated_otp = ''
            for i in range(6):
                generated_otp += secrets.choice(string.digits)

            if generated_otp == '':
                raise Exception('Invalid token.')
            else:
                token = AccessToken(owner=user, type=type, token=generated_otp, lifespan=lifespan)

                subject = 'Your Diamond Hands OTP'
                body = f""" Dear {user.profile.first_name},
    
                        You have requested for a One-Time Password (OTP).
                        
                        Your OTP is {token.token}
    
                        If you did not make this request, or have any queries about your account, please contact us at +65-6235 3535.
                        
                        Yours Sincerely,
                        Diamond Hands Team
                        """
        elif type == 'VERIFY' or 'RESETPW':
            token = AccessToken(owner=user, type=type, token=str(uuid4()), lifespan=lifespan)
            if type == 'VERIFY':
                subject = 'Verify your email address on Diamond Hands'
                action = 'Verify your email'
                url = f'https://taurus.sitict.net/verifyCheck/{token.token}'
            else:
                subject = 'Reset your password on Diamond Hands'
                action = 'Reset your password'
                url = f'https://taurus.sitict.net/resetPassword/{token.token}'
            body = f""" Dear {user.profile.first_name},

                    You've entered {user.email} as your Diamond Hands email address.
    
                    {action} by clicking on the following link:
                    {url}

                    Yours Sincerely,
                    Diamond Hands Team
                    """
        else:
            raise Exception('Invalid token type.')

        Authentication.send_email(user.email, subject, body)
        token.save()

    def verify_token(self, token_str):
        """
            Function to verify if an access token is valid or not

            @params:
                self, the access token model object
                token_str, the access token
            @returns: the user object which is the owner of the access token
        """
        try:
            token = self.get(token=token_str)
            if token.check_expired():
                raise Exception('Token has expired')
            else:
                return token.owner
        except ObjectDoesNotExist:
            raise Exception('Invalid token.')

    def expire_token(self, uuid):
        """
            Function to expire the access token based on the uuid

            @params:
                self, the access token model object
                uuid, the access token object
        """
        token = self.get(token=uuid)
        token.set_expired()

    def expire_old_token(self, user, access_type):
        """
            Function to expire the latest access token tag to the user object and access type params

            @params:
                self, the access token model object
                user, user object
                access_type, the type of the access token i.e. RESETPW, VERIFY, OTP
        """
        try:
            latest = self.filter(owner=user, type=access_type).latest('date_created')
            latest.set_expired()
        except ObjectDoesNotExist:
            print("No token exists")


class AccessToken(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=25)
    token = models.CharField(max_length=36)
    date_created = models.DateTimeField(auto_now_add=True)
    lifespan = models.IntegerField()
    expired = models.BooleanField(default=False)
    objects = AccessTokenManager()

    def check_expired(self):
        """
            Function to check if the access token is expired

            @params: self, the access token model object
            @returns: a bool true if expired and false if not
        """
        age = (datetime.now(timezone.utc) - self.date_created).total_seconds() / 60.0
        if age > self.lifespan:
            self.expired = True
            self.save()
        return self.expired

    def set_expired(self, expired=True):
        """
            Function to set access token to expired

            @params:
                self, the access token model object
                expired, a True bool variable
        """
        self.expired = expired
        self.save()

    def __str__(self):
        return self.token


class Authentication():
    """
        An Authentication class to hold all the authenticating logic on the webserver

        class functions available:
            - register(data)
            - is_human(captcha_response)
            - retrieveVerifierSalt(email)
            - send_email(email, subject, body)
    """

    @staticmethod
    def register(data):
        """
            Function to create a user and user profile object and save them to the database.

            @params:
                data, a dictionary containing the POST data from client-side
            @returns:
                user, the newly created user object based on data
        """
        if Validation_Functions.validate_register(data):
            if data['password'] == data['confirm_password']:
                # check if DB has existing email
                try:
                    User.objects.get(email=data['email'])
                    raise ValueError('User exists in the database!')
                except ObjectDoesNotExist:
                    # Create and populate user object
                    user = User(email=data['email'])
                    user.set_password(password=data["password"], salt=data["salt"])

                    # Insert into MySQL DB
                    user.save()

                    # Create and populate user profile object
                    user_profile = Profile(first_name=data["firstName"], last_name=data["lastName"], owner=user,
                                            date_of_birth=datetime.strptime(data["dob"], "%d/%m/%Y"))

                    # Insert user profile into MySQL DB
                    user_profile.save()

                    return user
            else:
                raise ValueError("Frontend validation failed, password do not match")
        else:
            raise ValueError("Frontend validation failed, possible bypass of Frontend validation")

    @staticmethod
    def is_human(captcha_response):
        """
            Function to validate reCAPTCHA response from google server

            @params:
                captcha_response, the captcha response from client-side
            @returns:
                Bool, return True if reCAPTCHA test passed for submitted form else returns False
        """
        secret = settings.GOOGL_RECAPTCHA_SECRET_KEY,
        payload = {'response': captcha_response, 'secret': secret}
        response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
        result = response.json()
        str_convert_result = str(result)

        if Validation.validate_google_api(str_convert_result):
            return True
        else:
            return False

    @staticmethod
    def retrieveVerifierSalt(email):
        """
            Function to retrieve the user password verifier and salt from database

            @returns:
                user.password, the password verifier of the user in the database
                user.salt, the salt of the user object
        """
        try:
            user = User.objects.get(email=email)
            return user.password, user.salt
        except ObjectDoesNotExist:
            return None, None

    @staticmethod
    def send_email(email, subject, body):
        """
            Function to send out emails to recipients

            @returns:
                user.password, the password verifier of the user in the database
                user.salt, the salt of the user object
        """
        port = settings.SMTP_PORT
        smtp_server = settings.SMTP_SERVER
        username = settings.SMTP_USERNAME
        password = settings.SMTP_PASSWORD
        sender_email = settings.SMTP_EMAIL

        message = Email.message.EmailMessage()
        message.add_header("From", sender_email)
        message.add_header("To", email)
        message.add_header("Subject", subject)
        message.set_content(body)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(username, password)
            server.sendmail(sender_email, email, message.as_string())


class Stock(models.Model):
    stock_symbol = models.CharField(max_length=15)
    company_name = models.CharField(max_length=100)
    company_desc = models.TextField(null=True)
    sector = models.CharField(max_length=45, null=True)
    industry = models.CharField(max_length=45, null=True)
    image_url = models.URLField(null=True)

    def __str__(self):
        return f'{self.stock_symbol} - {self.company_name}'


class StockPriceCurManager(models.Manager):
    def update_prices(self):
        """
            Function to update the current price of the stock in the database

            @params:
                self, the stock price object model
        """
        stocks = self.all()
        print(f'Updating Stock Prices:')
        for stock_price in stocks:
            ticker = yf.Ticker(stock_price.stock.stock_symbol)
            ticker_info = ticker.history(period='1mo')
            if ticker_info.empty:
                stock_price.stock.delete()
            else:
                index = -1
                while(True):
                    stock_price.open = ticker_info.get('Open')[index]
                    stock_price.close = ticker_info.get('Close')[index]
                    stock_price.high = ticker_info.get('High')[index]
                    stock_price.low = ticker_info.get('Low')[index]
                    try:
                        stock_price.save()
                        break
                    except Exception:
                        index -= 1

        print(f'Stock Price Update Complete')

    def get_current_price(self, stock):
        """
            Function to update the current price of the stock in the database

            @params:
                self, the stock price object model
                stock, the stock object of the current price
            @returns:
                the stock price object current price
        """
        return self.get(stock=stock).close


class StockPriceCurrent(models.Model):
    stock = models.OneToOneField(
        Stock,
        on_delete=models.CASCADE
    )
    open = models.DecimalField(max_digits=8, decimal_places=3, null=True)
    close = models.DecimalField(max_digits=8, decimal_places=3, null=True)
    high = models.DecimalField(max_digits=8, decimal_places=3, null=True)
    low = models.DecimalField(max_digits=8, decimal_places=3, null=True)
    objects = StockPriceCurManager()

    def __str__(self):
        return f'{self.stock.stock_symbol} - {self.stock.company_name}'


class FavouriteManager(models.Manager):
    def set_favourite(self, user, stock, set=True):
        """
            Function to favourite or unfavourite a particular stock for the owner.

            @params:
                self, the favourite object model
                user, the user object
                stock, the stock object
                set, True by default
        """
        if set:
            favourite = Favourites(owner=user, stock=stock)
            favourite.save()
        else:
            favourite = self.get(owner=user, stock=stock)
            favourite.delete()

    def is_favourite(self, user, stock):
        """
            Function to retrieve if the user has favourite the stock or not

            @params:
                self, the favourite object model
                user, the user object
                stock, the stock object
            @returns:
                True if the stock is favourite by user or False if there is not
        """
        try:
            return self.filter(owner=user, stock=stock).exists()
        except Exception:
            return False

    def get_favourites(self, user):
        """
            Function to retrieve all the stock the user has favourite

            @params:
                self, the favourite object model
                user, the user object
            @returns:
                all the stock object that has been favourite by the user or false if there is None
        """
        return self.filter(owner=user)


class Favourites(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    objects = FavouriteManager()

    def __str__(self):
        return f'{self.owner.profile.first_name} - {self.stock.company_name}'


class TransactionManager(models.Manager):
    def get_user_transactions(self, user):
        """
            Function to retrieve all the transaction the user has

            @params:
                self, the transaction object model
                user, the user object
            @returns:
                all the transaction object that the user has
        """
        return self.filter(owner=user)

    def get_active_transactions(self, user, active=True, stock=None, option=None):
        """
            Function to retrieve all the active transaction the user has

            @params:
                self, the transaction object model
                user, the user object
                active, the transaction is active, True on default
                stock, get a specific stock that is active, None by default
                option, get the specific option stock (BUY/SELL), None by default
            @returns:
                all the transaction object that the user by the specifications
        """
        try:
            if option and stock:
                return self.filter(owner=user, stock=stock, active=active, option=option)
            elif option:
                return self.filter(owner=user, active=active, option=option)
            elif stock:
                return self.filter(owner=user, stock=stock, active=active)
            else:
                return self.filter(owner=user, active=active)
        except:
            return None

    def purchase_option(self, user, stock, option, quantity):
        """
            Function to allow users to make a option purchase of the stock

            @params:
                self, the transaction object model
                user, the user object
                stock, the stock object
                option, the type of option (BUY/SELL)
                quantity, how many shares of the stock to purchase
        """
        stock_price = StockPriceCurrent.objects.get_current_price(stock)
        total_price = stock_price * quantity
        isvalid, msg = Validation_Functions.validate_purchase_option(quantity, total_price,
                                                                     user.profile.account_balance)
        if isvalid:
            user.profile.account_balance -= total_price
            active_transaction = self.get_active_transactions(user, True, stock, option)

            if active_transaction.exists():
                transaction = active_transaction.first()
                transaction.price = (transaction.price * transaction.lot_quantity + stock_price * quantity) / (
                        transaction.lot_quantity + quantity)
                transaction.lot_quantity += quantity
                transaction.transaction_date = datetime.now(timezone.utc)
            else:
                transaction = Transaction(owner=user, stock=stock, option=option, lot_quantity=quantity)
                transaction.price = stock_price

            user.profile.save()
            transaction.save()
        else:
            raise Exception(msg)

    def sell_option(self, user, stock, option, quantity):
        """
            Function to allow users to sell their existing active of the stock

            @params:
                self, the transaction object model
                user, the user object
                stock, the stock object
                option, the type of option (BUY/SELL)
                quantity, how many shares of the stock to sell
        """
        active_transaction = self.get_active_transactions(user, True, stock, option)
        if active_transaction.exists():
            owned_transaction = active_transaction.first()

            isvalid, msg = Validation_Functions.validate_sell_option(quantity, owned_transaction.lot_quantity)
            if isvalid:
                owned_transaction.lot_quantity -= quantity
                stock_price = StockPriceCurrent.objects.get_current_price(stock)

                sell_transaction = Transaction(owner=user, stock=stock, option=option,
                                                    lot_quantity=quantity,
                                                    active=False, price=stock_price)
                sell_transaction.save()

                sell_price = stock_price * quantity
                purchase_price = owned_transaction.price * quantity
                difference = purchase_price - sell_price
                user.profile.account_balance += sell_price if option == 'BUY' else difference + purchase_price

                owned_transaction.save()
                user.profile.save()
            else:
                raise Exception(msg)
        else:
            raise Exception(f'You do not own any shares of this stock!')

    def delete_user_transactions(self, user):
        self.filter(owner=user).delete()


class Transaction(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=8, decimal_places=3)
    lot_quantity = models.IntegerField()
    option = models.CharField(max_length=10)
    active = models.BooleanField(default=True)
    objects = TransactionManager()

    def __str__(self):
        return f'{self.owner.profile.first_name} - {self.stock.company_name}'

    def get_stock_industry(self):
        return self.stock.industry
