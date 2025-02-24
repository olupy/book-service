from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import AuditableModel
from .enums import RoleEnum


class User(AbstractBaseUser, PermissionsMixin, AuditableModel):
    firstname = models.CharField(max_length=100, null=True)
    lastname = models.CharField(max_length=100, null=True)
    email = models.EmailField(_('email address'), unique=True, db_index=True)
    phone = models.CharField(max_length=17, null=True, unique=True, blank=True)
    password = models.CharField(max_length=600, null=True)
    role = models.CharField(max_length=100, null=True, choices= RoleEnum.choices())
    is_active = models.BooleanField(default=True)
    objects = models.Manager()
