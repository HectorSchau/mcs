from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

# Create your models here.
class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="plazoleta_users_groups",  # Cambia el related_name
        related_query_name="plazoleta_user",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name="plazoleta_users_permissions",  # Cambia el related_name
        related_query_name="plazoleta_user",
    )

    def __str__(self):        
        return f"{self.id}: {self.username}"      
    pass





