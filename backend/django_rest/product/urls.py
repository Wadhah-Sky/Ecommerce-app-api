from django.urls import path

from product import views


# Define a variable that help to identify which api that creating URL from when
# using reverse function.
app_name = 'product'

urlpatterns = [
    path(
        'product/details/<slug:slug>/',
        views.ProductRetrieveAPIView.as_view(),
        name='specific-product-details'
    ),
]
