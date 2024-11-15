from django.contrib import admin

from .models import User, Category, Ad, Response

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Ad)
admin.site.register(Response)
