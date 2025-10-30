from rest_framework.test import APITestCase
from configapp.models import *
from django.urls import reverse
from rest_framework import status
class ProductViewSetTestCase(APITestCase):
    # python manage.py dumpdata configapp.Category - -format = yaml - -indent = 4 > configapp / fixtures / categories.yaml

    def setUp(self):
        self.user = User.objects.create_user(email = 'rustam@gmail.com',password = '1111')
        self.staff_user = User.objects.create_user(email = 'anvar@gmail.com',password = '7777',is_staff = True)

        self.category1 = Category.objects.create(name = "Electronics")
        self.category2 = Category.objects.create(name = "Books")

        self.product1 = Product.objects.create(name = "Laptop",description = "Powerful Laptop",category = self.category1,price= 5000)
        self.product2 = Product.objects.create(name = "Book",description = "Thriller Book",category = self.category2,price = 10000)

        Review.objects.create(product = self.product1,rating = 5,user_id = 1)
        Review.objects.create(product = self.product2,rating = 4,user_id = 2)
        Review.objects.create(product = self.product1,rating = 3,user_id = 1)

    def test_product_list(self):
        url = reverse('products-list')
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_product_filter_by_category(self):
        url = reverse('products-list') + "?category=" + str(self.category1.id)
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']),1)

    def test_product_detail(self):
        url = reverse('products-detail',args = [self.product1.id])
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['product']['name'],'Laptop')

    def test_top_rated(self):
        url = reverse('products-top-rated')
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'],'Laptop')
    def test_average_rating(self):
        url = reverse('products-average-rating',args=[self.product1.id])
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['avg_rating'],4)

    def test_permission_denied_for_anonymous_create(self):
        self.client.force_authenticate(user = None)
        url = reverse('products-list')
        data = {'name':'Test Product','description':'This is a test for products','price':1000}
        response = self.client.post(url,data,format = 'json')
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_permission_granted_for_staff(self):
        self.client.force_authenticate(self.staff_user)
        url = reverse('products-list')
        data = {'name':'Test Product','description':'This is a test for products','price':1000}
        response = self.client.post(url,data,format = 'json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

