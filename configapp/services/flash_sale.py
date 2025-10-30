from datetime import datetime,timedelta
from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from configapp.serializers import *
class FlashSaleListCreateView(generics.ListCreateAPIView):
    queryset = FlashSale.objects.all()
    class FlashSaleSerializer(serializers.ModelSerializer):
        class Meta:
            model = FlashSale
            fields = ('id','product','discount_percentage','start_time','end_time')
    serializer_class = FlashSaleSerializer
class Check_SaleApi(APIView):
    def get(self,request,pk):
        product = get_object_or_404(Product,pk = pk)
        user_viewed = ProductViewHistory.objects.filter(user = request.user,product = product).exists()
        upcoming_flash_sale = FlashSale.objects.filter(product=product,start_time__lte = datetime.now() + timedelta(hours=24)).first()
        if user_viewed and upcoming_flash_sale:
            discount = upcoming_flash_sale.discount_percentage
            start_time = upcoming_flash_sale.start_time
            end_time = upcoming_flash_sale.end_time
            return Response({
                'message':f"This product will be on a {discount}% of flash sale",
                'start_time':start_time,
                'end_time':end_time,
            })
        else:
            return Response({
                "message":"No upcoming flash sale for this product"
            })










