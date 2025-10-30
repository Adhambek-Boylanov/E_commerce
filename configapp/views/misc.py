from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from configapp.permissions import *
from configapp.models import Review, Category,Order
from configapp.serializers import ReviewSerializer, CategorySerializer,OrderSerializer


class CustomPagination(PageNumberPagination):
    page_size = 2

class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class OrderViewsSet(ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
