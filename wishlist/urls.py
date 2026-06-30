from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.views import profile_view, register_view
from wishlists.views import (
    wishlist_create_view,
    wishlist_detail_view,
    wishlist_item_create_view,
    wishlist_list_view,
)


urlpatterns = [
    path("admin/", admin.site.urls),

    path("", wishlist_list_view, name="home"),

    path("register/", register_view, name="register"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", profile_view, name="profile"),

    path("wishlists/", wishlist_list_view, name="wishlist_list"),
    path("wishlists/create/", wishlist_create_view, name="wishlist_create"),
    path("wishlists/<int:pk>/", wishlist_detail_view, name="wishlist_detail"),
    path(
        "wishlists/<int:wishlist_pk>/items/create/",
        wishlist_item_create_view,
        name="wishlist_item_create",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)