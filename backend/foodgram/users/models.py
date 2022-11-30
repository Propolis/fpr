from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'USR'
    ADMIN = 'ADM'
    USER_ROLE_CHOICES = [
        (USER, 'user'),
        (ADMIN, 'admin')
    ]

    role = models.CharField(
        max_length=3,
        verbose_name="Роль",
        choices=USER_ROLE_CHOICES,
        default='USR',
        blank=False,
    )

    username = models.CharField(
        verbose_name="Имя пользователя", max_length=32, unique=True
    )
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

    @property
    def is_admin(self):
        return self.role == self.ADMIN
