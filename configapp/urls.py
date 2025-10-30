from . import signals
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from configapp.services import *
from configapp.services import admin_replenish_stock
from .views import *
router = DefaultRouter()
router.register(r'categories',CategoryViewSet,basename="categories")
router.register(r'products',ProductViewSet,basename="products")
router.register(r'reviews',ReviewViewSet,basename="reviews")
router.register(r'orders',OrderViewsSet,basename="orders")
urlpatterns = [
    path('',include(router.urls)),
    path('flashe_sale/',FlashSaleListCreateView.as_view()),
    path('check_sale/<int:pk>/',Check_SaleApi.as_view()),
    path('product_view/',ProductViewCreate.as_view()),
    path('send_sms/',SendSmsApi.as_view(),name = 'sms_kod'),
    path('verify_check/',VerifyApi.as_view(),name = 'verify_check'),
    path('replenish_stock/<int:product_id>/<int:amount>/',admin_replenish_stock,name = 'replenish_stock'),
    re_path(r'^auth/', include('djoser.urls')),
]