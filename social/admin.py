from django.contrib import admin

from .models import FriendRequest, Relationship


admin.site.register(FriendRequest)
admin.site.register(Relationship)