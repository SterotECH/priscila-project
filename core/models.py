"""
Database model for Core
"""

import os
import random
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.manager import UserManager
from rest_framework_simplejwt.tokens import RefreshToken


AUTH_PROVIDERS = {
    'facebook': 'facebook',
    'google': 'google',
    'twitter': 'twitter',
    'email': 'email'
}

class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('presiding_elder', 'Presiding Elder'),
        ('supporting_elder', 'Supporting Elder'),
        ('financial_secretary', 'Financial Secretary'),
        ('secretary', 'Secretary'),
        ('executive member ', 'Executive Member'),
    )
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("Username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 10 characters or fewer"
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that staff ID already exists."),
        })
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        }
    )
    name = models.CharField(_("full name"), max_length=255)
    contact = models.CharField(
        _("contact"), max_length=20, blank=True, unique=True)
    user_type = models.CharField(_("User Type"), max_length=50, choices=USER_TYPE_CHOICES)
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site.")
    )
    is_verified = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))


    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["name", "email"]

    def __str__(self) -> str:
        return f'{self.username} - {self.name}'


    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    class Meta:
        ordering = ["-id"]
