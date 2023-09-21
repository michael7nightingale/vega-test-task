from tortoise import fields

import random

from .base import TortoiseModel


def generate_identifier() -> str:
    return "".join(str(random.randint(0, 9)) for _ in range(8))


class User(TortoiseModel):
    id = fields.CharField(pk=True, default=generate_identifier, max_length=8)
    fio = fields.CharField(max_length=120)
    phone = fields.CharField(max_length=10, index=True, unique=True)
    email = fields.CharField(unique=True, index=True, max_length=100)
    password = fields.CharField(max_length=255)

    companies = fields.ManyToManyField("models.Company", related_name="users")


class UserSettings(TortoiseModel):
    user = fields.OneToOneField("models.User", related_name="settings")
    wifi_load_only = fields.BooleanField(default=True)
    extra_authentication = fields.BooleanField(default=False)
    images_twice = fields.BooleanField(default=False)
