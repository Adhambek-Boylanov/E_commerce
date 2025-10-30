from rest_framework.test import APITestCase
from configapp.models import *
from django.urls import reverse
from rest_framework import status
class CategoryTestCase(APITestCase):
    fixtures = ["categories"]
    def setUp(self):
        self.user = User.objects.create_user(email="adhambek@gmail.com",password='1906')
        self.client.force_authenticate(user = self.user)
        self.category1 = Category.objects.first()
    def test_category_list(self):
        url = reverse('categories-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),4)

    def test_category_detail(self):
        url = reverse('categories-detail',args=[self.category1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_category_create(self):
        url = reverse('categories-list')
        data = {"name":"Book"}
        response = self.client.post(url,data,format="json")
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_category_update(self):
        url = reverse('categories-detail',args=[self.category1.pk])
        data = {"name":"Electronic gadgets"}
        response = self.client.put(url,data,format="json")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    def test_category_delete(self):
        url = reverse('categories-detail',args=[self.category1.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)



