from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from configapp.serializers import ProductViewSerializer, ProductSerializer

class ProductViewCreate(APIView):
    @swagger_auto_schema(request_body=ProductViewSerializer)
    def post(self,request):
        serializer = ProductViewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user = request.user)
        return Response(data=serializer.data,status=status.HTTP_201_CREATED)