from django.urls import path
from payment import views

# Define a variable that help to identify which api that creating URL from when
# using reverse function.
app_name = 'payment'

urlpatterns = [
    path(
        'payment/methods/',
        views.PaymentMethodListAPIView.as_view(),
        name='payment-method-list'
    )
]
