from django.contrib import admin

from .models import Wishlist, WishlistAccess, WishlistItem


admin.site.register(Wishlist)
admin.site.register(WishlistAccess)
admin.site.register(WishlistItem)