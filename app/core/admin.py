"""Customize and manage your project django admin web page"""

from django.contrib import admin
from core import models


admin.site.register(models.Category)
