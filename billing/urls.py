from django.urls import path

from billing.views import CreateChargeView

urlpatterns = [
path('pay/', CreateChargeView.as_view(), name='create-charge'),

]
