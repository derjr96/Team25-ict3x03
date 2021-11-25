from django.test import TestCase, Client
from django.urls import reverse, resolve
from ..views import home, login, register, portfolio, history, profile, users, staffUserProfile, stockDetails
from datetime import datetime
from ..models import User, Profile, Stock, StockPriceCurrent


class Test_NonUserRequired_Urls(TestCase):
    """
    Things to test:
        - A non authenticated user tries to access index page -> Done
        - A non authenticated user tries to access login page -> Done
        - A non authenticated user tries to access register page -> Done
        - A non authenticated user tries to access stock detail page -> Done
    """

    def setUp(self):
        super().setUp()
        self.client = Client()
        self.stock = Stock(company_name="TESLA", company_desc="This is a test",
                           image_url="https://imgur.com/gallery/KT1kwRV",
                           stock_symbol="TSLA", sector="Transport", industry="Transport")
        self.stock.save()
        self.stock_price = StockPriceCurrent(high=0.012, low=0.012, open=0.012, close=0.012, stock=self.stock)
        self.stock_price.save()

    def test_index_url(self):
        """
            A non authenticated user tries to access index page

            The user will be redirected to index page
        """
        url = reverse('index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(resolve(url).func, home)
        self.assertTemplateUsed(response, 'index.html')

    def test_login_url(self):
        """
            A non authenticated user tries to access login page

            The user will be redirected to login page
        """
        url = reverse('login')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(resolve(url).func, login)
        self.assertTemplateUsed(response, 'login.html')

    def test_register_url(self):
        """
            A non authenticated user tries to access register page

            The user will be redirected to register page
        """
        url = reverse('register')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(resolve(url).func, register)
        self.assertTemplateUsed(response, 'register.html')

    def test_stock_detail_url(self):
        """
            A non authenticated user tries to access stock detail page

            The user will be redirected to stock detail page
        """
        url = reverse('stockDetails', args=(self.stock.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(resolve(url).func, stockDetails)
        self.assertTemplateUsed(response, 'stockDetails.html')


class Test_UserRequiredUrls_WithAuthenticatedUser(TestCase):
    """
    Things to test:
        - A student user tries to access portfolio page -> Done
        - A teacher user tries to access student's portfolio page -> Done
        - A student user tries to access history page -> Done
        - A teacher user tries to access student's history page -> Done
        - A student user tries to access profile page -> Done
        - A teacher user tries to access user list page -> Done
        - A teacher user tries to access staff user profile page -> Done
        - A student user tries to access login page -> Done
        - A student user tries to access register page -> Done
    """

    def setUp(self):
        super().setUp()
        self.client = Client()

        # Set up Teacher Account
        self.teacher = User.objects.create(email='teacher@gmail.com', is_staff=True)
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

    def test_student_access_portfolio_url(self):
        """
            A student user tries to access portfolio page

            The user will be redirected to portfolio page
        """
        self.client.force_login(self.student)
        url = reverse('portfolio')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(resolve(url).func, portfolio)
        self.assertTemplateUsed(response, 'portfolio.html')

    def test_teacher_access_portfolio_with_args_url(self):
        """
            A teacher user tries to access student's portfolio page

            The user will be redirected to student's portfolio page
        """
        self.client.force_login(self.teacher)
        url = reverse('portfolio-staff', args=(self.student.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(resolve(url).func, portfolio)
        self.assertTemplateUsed(response, 'portfolio.html')

    def test_student_access_history_url(self):
        """
            A student user tries to access history page

            The user will be redirected to history page
        """
        self.client.force_login(self.student)
        url = reverse('history')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(resolve(url).func, history)
        self.assertTemplateUsed(response, 'history.html')

    def test_teacher_access_history_with_args_url(self):
        """
            A teacher user tries to access student's history page

            The user will be redirected to student's history page
        """
        self.client.force_login(self.teacher)
        url = reverse('history-staff', args=(self.student.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(resolve(url).func, history)
        self.assertTemplateUsed(response, 'history.html')

    def test_student_access_profile_url(self):
        """
            A student user tries to access profile page

            The user will be redirected to profile page
        """
        self.client.force_login(self.student)
        url = reverse('profile')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(resolve(url).func, profile)
        self.assertTemplateUsed(response, 'profile.html')

    def test_teacher_access_student_list_url(self):
        """
            A teacher user tries to access user list page

            The user will be redirected to user list page
        """
        self.client.force_login(self.teacher)
        url = reverse('users')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(resolve(url).func, users)
        self.assertTemplateUsed(response, 'users.html')

    def test_teacher_access_staff_user_profile_url(self):
        """
            A teacher user tries to access staff user profile page

            The user will be redirected to staff user profile page
        """
        self.client.force_login(self.teacher)
        url = reverse('staffUserProfile', args=(self.student.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(resolve(url).func, staffUserProfile)
        self.assertTemplateUsed(response, 'staffUserProfile.html')

    def test_authenticated_user_access_login_url(self):
        """
            A student user tries to access login page

            The user will be redirected to index page
        """
        self.client.force_login(self.student)
        url = reverse('login')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_access_register_url(self):
        """
            A student user tries to access register page

            The user will be redirected to index page
        """
        self.client.force_login(self.student)
        url = reverse('register')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)


class Test_UserRequiredUrls_WithNonAuthenticatedUser(TestCase):
    """
    Things to test:
        - A non authenticated user tries to access portfolio over URL-> Done
        - A non authenticated user tries to access history over URL -> Done
        - A non authenticated user tries to access profile over URL -> Done
        - A non authenticated user tries to access user list over URL -> Done
    """

    def setUp(self):
        super().setUp()
        self.client = Client()

    def test_non_authenticated_user_access_portfolio_url(self):
        """
            A non authenticated user tries to access portfolio over URL

            The user will be redirected to index page
        """
        url = reverse('portfolio')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_non_authenticated_user_access_history_url(self):
        """
            A non authenticated user tries to access history over URL

            The user will be redirected to index page
        """
        url = reverse('history')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_non_authenticated_user_access_profile_url(self):
        """
            A non authenticated user tries to access profile over URL

            The user will be redirected to index page
        """
        url = reverse('profile')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_non_authenticated_user_access_student_list_url(self):
        """
            A non authenticated user tries to access user list over URL

            The user will be redirected to index page
        """
        url = reverse('users')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
