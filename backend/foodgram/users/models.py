from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    USER_ROLE_CHOICES = [
        (USER, 'USR'),
        (ADMIN, 'ADM'),
    ]

    role = models.CharField(
        max_length=3,
        verbose_name="Роль",
        choices=USER_ROLE_CHOICES,
        default=USER,
        blank=False,
    )

    username = models.CharField(
        verbose_name="Имя пользователя", max_length=150, null=True, unique=True
    )
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    @property
    def is_admin(self):
        return self.role == self.ADMIN
