from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Production)
admin.site.register(Product)