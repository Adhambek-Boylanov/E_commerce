from rest_framework import serializers
from configapp.models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    avg_rating = serializers.FloatField(read_only=True,required=False)
    class Meta:
        model = Product
        fields = ['id','name','avg_rating','description','stock','price','category']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"

class ProductViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductViewHistory
        fields = ('user','product')
        read_only_fields = ['user']
