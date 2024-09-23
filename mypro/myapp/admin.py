from django.contrib import admin
from .models import Profile
from .models import Customer, Extended

# Register your models here.

admin.site.register(Profile)
admin.site.register(Customer)
admin.site.register(Extended)
