from django.urls import path
from order import views

# Define a variable that help to identify which api that creating URL from when
# using reverse function.
app_name = 'order'

urlpatterns = [
    path(
        'order/check/',
        views.PurchaseOrderCheckAPIView.as_view(),
        name='purchase-order-check'
    ),
    path(
        'order/create/',
        views.PurchaseOrderCreateAPIView.as_view(),
        name='purchase-order-create'
    ),
    path(
        'order/template/details/<slug:po_code>/',
        views.PurchaseOrderRetrieveTemplateAPIView.as_view(),
        name='specific-purchase-order-details-template'
    ),
]
