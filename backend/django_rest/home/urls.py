from django.urls import path
from home import views

# Define a variable that help to identify which api that creating URL from when
# using reverse function.
app_name = 'home'

urlpatterns = [
    path(
        'home/',
        views.HomeListAPIView.as_view(),
        name='home-list'
    )
]
