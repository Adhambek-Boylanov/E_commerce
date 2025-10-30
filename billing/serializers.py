from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['order','amount','stripe_charge_id']
        read_only_fields = ['amount']
