"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static

from core.views import IndexTemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('_nested_admin/', include('nested_admin.urls')),

    path('api-auth/',
         include('rest_framework.urls', namespace='rest_framework')),

    path('api/v1/', include('core.urls')),
    path('api/v1/', include('home.urls')),
    path('api/v1/', include('store.urls')),
]

# in case running on development server, can access media files urls.
# in case running on production server so 'DEBUG' is False, nginx proxy will
# handle media files urls.
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

urlpatterns.append(re_path(r'^.*$', IndexTemplateView.as_view(), name='index'))
