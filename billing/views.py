from django.shortcuts import render
import stripe
from rest_framework.response import Response

from .models import Payment
from .serializers import PaymentSerializer
from configapp.models import Order
from rest_framework import views,status
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateChargeView(views.APIView):
    @swagger_auto_schema(request_body=PaymentSerializer)
    def post(self,request,*args,**kwargs):
        stripe_token = request.data.get('stripe_token')
        order_id = request.data.get('order_id')
        order = get_object_or_404(Order,pk = order_id)
        try:
            total_amount = order.product.price * order.quantity
            charge = stripe.Charge.create(
                amount = int(total_amount * 100),
                currency = "usd",
                source = stripe_token,
            )

            Payment.objects.create(
                order = order,
                stripe_charge_id = charge["id"],
                amount = total_amount
            )
            order.is_paid = True
            order.save()
            return Response({"status":"Payment successfully"},status =status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)},status = status.HTTP_400_BAD_REQUEST)





