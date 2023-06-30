"""Register your backend views"""

from django.urls import path

from cart import views

# Define a variable that help to identify which api that creating URL from when
# using reverse function.
app_name = 'cart'

urlpatterns = [
    path(
        'cart/check/',
        views.CartCheckApiView.as_view(),
        name='cart-check',
    ),
]
