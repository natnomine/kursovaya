from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField("self", blank=True, verbose_name="Друзья")
    avatar = models.ImageField("Аватарка", blank=True, null=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        default_related_name = "profile"

    def __str__(self):
        return self.user.username


class Chat(models.Model):
    name = models.CharField("Название", max_length=128)
    members = models.ManyToManyField(UserProfile, verbose_name="Участники")
    is_private = models.BooleanField("Личная переписка?", default=False)

    class Meta:
        verbose_name = "Беседа"
        verbose_name_plural = "Беседы"

    def __str__(self):
        return self.name


class Message(models.Model):
    text = models.TextField("Текст")
    sender = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    chat = models.ForeignKey(Chat, models.CASCADE)
    send_at = models.DateTimeField("Дата создания контракта", auto_now_add=True)

    class Meta:
        ordering = ['send_at']
        default_related_name = "messages"
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return f"Сообщения от '{self.sender}'"
