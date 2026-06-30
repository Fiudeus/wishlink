from django.conf import settings
from django.db import models


class Wishlist(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wishlists",
        verbose_name="Владелец",
    )
    title = models.CharField("Название", max_length=100)
    description = models.TextField("Описание", blank=True)
    is_public = models.BooleanField("Публичный", default=False)
    allowed_relation_types = models.JSONField(
        "Типы отношений с доступом",
        default=list,
        blank=True,
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Вишлист"
        verbose_name_plural = "Вишлисты"

    def __str__(self):
        return self.title


class WishlistAccess(models.Model):
    wishlist = models.ForeignKey(
        Wishlist,
        on_delete=models.CASCADE,
        related_name="custom_accesses",
        verbose_name="Вишлист",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wishlist_accesses",
        verbose_name="Пользователь",
    )

    class Meta:
        verbose_name = "Ручной доступ к вишлисту"
        verbose_name_plural = "Ручные доступы к вишлистам"
        constraints = [
            models.UniqueConstraint(
                fields=["wishlist", "user"],
                name="unique_wishlist_access",
            )
        ]

    def __str__(self):
        return f"{self.user} имеет доступ к {self.wishlist}"


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(
        Wishlist,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Вишлист",
    )
    name = models.CharField("Название", max_length=100)
    description = models.TextField("Описание", blank=True)
    product_url = models.URLField("Ссылка на товар", blank=True)
    image = models.ImageField(
        "Загруженное изображение",
        upload_to="wishlist_items/",
        blank=True,
        null=True,
    )
    image_url = models.URLField("Ссылка на изображение", blank=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Предмет вишлиста"
        verbose_name_plural = "Предметы вишлистов"

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        return self.image_url

    @property
    def image_warning(self):
        if self.image and self.image_url:
            return "Будет использован загруженный файл."
        return ""

    def __str__(self):
        return self.name