from django.urls import path
from shipping import views

# Define a variable that help to identify which api that creating URL from when
# using reverse function.
app_name = 'shipping'

urlpatterns = [
    path(
        'shipping/countries/',
        views.ShippingCountryListAPIView.as_view(),
        name='shipping-country-list'
    ),
    path(
        'shipping/methods/',
        views.ShippingMethodListAPIView.as_view(),
        name='shipping-method-list'
    ),
    path(
        'shipping/cost/',
        views.ShippingCostAPIView.as_view(),
        name='shipping-cost'
    )
]
