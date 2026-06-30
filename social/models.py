from django.conf import settings
from django.db import models


class FriendRequest(models.Model):
    STATUS_PENDING = "pending"
    STATUS_ACCEPTED = "accepted"
    STATUS_DECLINED = "declined"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Ожидает"),
        (STATUS_ACCEPTED, "Принята"),
        (STATUS_DECLINED, "Отклонена"),
    ]

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_friend_requests",
        verbose_name="Отправитель",
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_friend_requests",
        verbose_name="Получатель",
    )
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Заявка в друзья"
        verbose_name_plural = "Заявки в друзья"
        constraints = [
            models.UniqueConstraint(
                fields=["sender", "receiver"],
                name="unique_friend_request",
            )
        ]

    def __str__(self):
        return f"{self.sender} → {self.receiver}: {self.get_status_display()}"


class Relationship(models.Model):
    FRIEND = "friend"
    BEST_FRIEND = "best_friend"
    PARTNER = "partner"
    FAMILY = "family"
    COLLEAGUE = "colleague"
    BLOCKED = "blocked"

    RELATION_TYPE_CHOICES = [
        (FRIEND, "Друг"),
        (BEST_FRIEND, "Лучший друг"),
        (PARTNER, "Партнёр"),
        (FAMILY, "Семья"),
        (COLLEAGUE, "Коллега"),
        (BLOCKED, "Заблокирован"),
    ]

    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="relationships_from",
        verbose_name="От пользователя",
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="relationships_to",
        verbose_name="К пользователю",
    )
    relation_type = models.CharField(
        "Тип отношения",
        max_length=30,
        choices=RELATION_TYPE_CHOICES,
        default=FRIEND,
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Отношение"
        verbose_name_plural = "Отношения"
        constraints = [
            models.UniqueConstraint(
                fields=["from_user", "to_user"],
                name="unique_relationship",
            )
        ]

    def __str__(self):
        return f"{self.from_user} → {self.to_user}: {self.get_relation_type_display()}"