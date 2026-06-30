from django import forms

from .models import Wishlist, WishlistItem


class WishlistForm(forms.ModelForm):
    allowed_relation_types_text = forms.CharField(
        required=False,
        help_text="Например: friend,best_friend,family",
        label="Типы отношений с доступом",
    )

    class Meta:
        model = Wishlist
        fields = ["title", "description", "is_public"]
        labels = {
            "title": "Название",
            "description": "Описание",
            "is_public": "Публичный",
        }

    def save(self, commit=True):
        wishlist = super().save(commit=False)

        raw = self.cleaned_data.get("allowed_relation_types_text", "")
        wishlist.allowed_relation_types = [
            item.strip()
            for item in raw.split(",")
            if item.strip()
        ]

        if commit:
            wishlist.save()

        return wishlist


class WishlistItemForm(forms.ModelForm):
    class Meta:
        model = WishlistItem
        fields = [
            "name",
            "description",
            "product_url",
            "image",
            "image_url",
        ]
        labels = {
            "name": "Название",
            "description": "Описание",
            "product_url": "Ссылка на товар",
            "image": "Загрузить изображение",
            "image_url": "Ссылка на изображение",
        }