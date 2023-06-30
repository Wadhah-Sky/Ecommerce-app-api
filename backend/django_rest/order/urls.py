from django.urls import path
from order import views

# Define a variable that help to identify which api that creating URL from when
# using reverse function.
app_name = 'order'

urlpatterns = [
    path(
        'order/create/',
        views.OrderAPIView.as_view(),
        name='order-create'
    ),
]
