from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Shop

from clothes.serializers import ShopSerializer


SHOP_URL = reverse('clothes:shop-list')


class PublicShopApiTests(TestCase):
    """Test the publicaly available shops API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(SHOP_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateShopApiTests(TestCase):
    """Test the authorized user shops API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'kikuchi.dai@gmail.com',
            'password',
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_shops(self):
        """Test retriving shops"""
        Shop.objects.create(user=self.user, name='Modern Blue',
                            link='modern_blue.com')
        Shop.objects.create(user=self.user, name='guji', link='guji.com')

        res = self.client.get(SHOP_URL)

        shops = Shop.objects.all().order_by('-name')

        serializer = ShopSerializer(shops, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_shops_limited_to_user(self):
        """Test that shops returned are for the authenticated user"""
        user2 = get_user_model().objects.create_user(
            'hana@gmail.com',
            'password2',
        )
        Shop.objects.create(user=user2, name='Fedeli official')
        shop = Shop.objects.create(user=self.user, name='Gransasso official')

        res = self.client.get(SHOP_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], shop.name)

    def test_create_shop_successful(self):
        """Test creating a new shop"""
        payload = {'name': 'guji', 'link': 'guji.com'}
        self.client.post(SHOP_URL, payload)

        exists = Shop.objects.filter(
            user=self.user,
            name=payload['name'],
            link=payload['link'],
        ).exists()

        self.assertTrue(exists)

    def test_create_shop_invalid(self):
        """Test creating a new shop with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(SHOP_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
