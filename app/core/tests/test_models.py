from django.test import TestCase
# get_user_model returns a user model that is currently active in project
from django.contrib.auth import get_user_model

from core import models


# def sample_user(email='kikuchi.dai@gmail.com', password='password'):
#     """Create a sample user"""
#     return get_user_model().objects.create_user(email, password)

def sample_category(user, name='Knit'):
    """Create a category"""
    return models.Category.objects.create(
            user=user,
            name=name
    )


class ModelTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='kikuchi.dai@gmail.com',
            password='password'
        )

    def test_create_user_with_email_successful(self):
        """Test Creating a new user with an email is successful"""
        email = 'kikuchi.dai@gmail.com'
        password = 'password'

        self.assertEqual(self.user.email, email)
        self.assertTrue(self.user.check_password(password))

    def test_new_user_email_normilized(self):
        """Test the email for a new user is normilized"""
        email = 'test@GMAIL.COM'

        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test Creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@gmail.com',
            'password'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=self.user,
            name='zanone'
        )

        self.assertEqual(str(tag), tag.name)

    def test_material_str(self):
        """Test the ingredient string representation"""
        material = models.Material.objects.create(
            user=self.user,
            name='cotton'
        )

        self.assertEqual(str(material), material.name)

    def test_shop_str(self):
        """Test the shop string representation"""
        shop = models.Shop.objects.create(
            user=self.user,
            name='Modern Blue',
        )
        self.assertEqual(str(shop), shop.name)

    def test_category_str(self):
        """Test the category string representation"""
        category = models.Category.objects.create(
            user=self.user,
            name='Knit'
        )
        self.assertEqual(str(category), category.name)

    def test_clothing_str(self):
        """Test the clothing string representation"""
        clothing = models.Clothing.objects.create(
            name='Gransass crewneck sweater',
            price='50000',
            description='a little bit tight, but very comfortable',
            category=sample_category(self.user),
            user=self.user
        )

        self.assertEqual(str(clothing), clothing.name)
