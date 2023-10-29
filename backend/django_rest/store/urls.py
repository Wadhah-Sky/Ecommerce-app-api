from django.urls import path
from rest_framework.routers import DefaultRouter
from store import views

# Important: the way path converters works is:
#
#       /prefix/<field_type(slug, str, int, uuid..etc):parameter_name>/suffix/

# Make an object of DefaultRouter class.
router = DefaultRouter()

# Define a variable that help to identify which api that creating URL from when
# using reverse function.
app_name = 'store'

urlpatterns = [
    path(
        'store/categories/',
        views.CategoryListAPIView.as_view(),
        name='store-category-list'
    ),
    path(
        'store/category/details/<slug:slug>/',
        views.CategoryRetrieveAPIView.as_view(),
        name='store-specific-category-details'
    ),
    path(
        'store/products/category/<slug:category_slug>/',
        views.ProductListAPIView.as_view(),
        name='store-specific-product-list'
    ),
    path(
        'store/attributes/category/<slug:category_slug>/',
        views.AttributeListAPIView.as_view(),
        name='store-specific-attribute-list'
    ),
    path(
        'store/search/<str:query>/',
        views.SearchAPIView.as_view(),
        name='store-search'
    )

]
