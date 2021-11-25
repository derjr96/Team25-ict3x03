from django.test import TestCase, Client
from ..models import User, Profile, Transaction
from django.urls import reverse
from datetime import datetime


class Test_User(TestCase):
    """
    Things to test:
        - Updating user's profile (first name and last name only) -> Done
        - Updating user's profile with a invalid first name and last name only -> Done
        - Teacher depositing virtual credits for student user -> Done
        - Teacher depositing more than 500 virtual credits for student user -> Done
        - Teacher deposited a negative virtual credits for student user -> Done
        - Teacher reset the student user account -> Done
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

    def test_update_profile(self):
        """
            Updating user's profile (first name and last name only)

            The first name and last name of user will be updated accordingly
        """
        self.client.force_login(self.student)
        response = self.client.post(reverse('profile'), {'fn': "Joker", 'ln': "Xue"})
        user = User.objects.get(email="student123@gmail.com")

        self.assertEqual(response.status_code, 200)
        self.assertEqual("Joker", str(user.profile.first_name))
        self.assertEqual("Xue", str(user.profile.last_name))

    def test_invalid_first_name_update_profile(self):
        """
            Updating user's profile with a invalid first name and last name only

            The first name and last name of user will not be updated
        """
        self.client.force_login(self.student)
        response = self.client.post(reverse('profile'), {'fn': "heloo99", 'ln': "Xue"})
        user = User.objects.get(email="student123@gmail.com")

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual("heloo99", str(user.profile.first_name))
        self.assertNotEqual("Xue", str(user.profile.last_name))

    def test_deposit_virtual_credits(self):
        """
            Teacher depositing virtual credits for student user

            The amount entered will be updated in the student users account accordingly
        """
        self.client.force_login(self.teacher)
        response = self.client.post(reverse('staffUserProfile', args=(self.student.id,)), {'deposit': 500})
        user = User.objects.get(email="student123@gmail.com")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(1500.00, user.profile.account_balance)

    def test_exceed_deposit_amount_of_virtual_credits(self):
        """
            Teacher depositing more than 500 virtual credits for student user

            The amount entered will not be update the student users account and will be rejected by the server
        """
        self.client.force_login(self.teacher)
        response = self.client.post(reverse('staffUserProfile', args=(self.student.id,)), {'deposit': 1000})
        user = User.objects.get(email="student123@gmail.com")

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(2000.00, user.profile.account_balance)

    def test_negative_deposit_amount_of_virtual_credits(self):
        """
            Teacher deposited a negative virtual credits for student user

            The amount entered will not be update the student users account and will be rejected by the server
        """
        self.client.force_login(self.teacher)
        response = self.client.post(reverse('staffUserProfile', args=(self.student.id,)), {'deposit': -50})
        user = User.objects.get(email="student123@gmail.com")

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(2000.00, user.profile.account_balance)

    def test_reset_account(self):
        """
            Teacher reset the student user account

            The student's account will be reset to orginal with $1000 virtual credits and
            remove all existing transactions.
        """
        self.client.force_login(self.teacher)
        response = self.client.post(reverse('staffUserProfile', args=(self.student.id,)), {'reset': 'reset'})
        user = User.objects.get(email="student123@gmail.com")

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Transaction.objects.filter(owner=user).exists())
        self.assertEqual(1000.00, user.profile.account_balance)

