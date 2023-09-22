from tortoise import fields
from tortoise.exceptions import IntegrityError

import random
from typing import Optional

from .base import TortoiseModel
from app.services.authentication import verify_password, hash_password


def generate_identifier() -> str:
    return "".join(str(random.randint(0, 9)) for _ in range(8))


class User(TortoiseModel):
    id = fields.CharField(pk=True, default=generate_identifier, max_length=8)
    fio = fields.CharField(max_length=120)
    phone = fields.CharField(max_length=10, index=True, unique=True)
    email = fields.CharField(unique=True, index=True, max_length=100)
    password = fields.CharField(max_length=255)

    companies = fields.ManyToManyField("models.Company", related_name="users")

    def __str__(self) -> str:
        return self.fio

    async def register(self, fio: str, phone: str, email: str, password: str) -> Optional["User"]:
        try:
            new_user = await self.create(
                fio=fio,
                phone=phone,
                email=email,
                password=hash_password(password)
            )
            await UserSettings.create(user=new_user
                                      )
            return new_user
        except IntegrityError:
            return None

    async def login(self, password: str, email: str | None = None, id_: str | None = None) -> Optional["User"]:
        if email is None and id_ is None:
            return None
        if email is not None and id_ is not None:
            return None
        statements = {"email": email} if email is not None else {"id": id_}
        user = await self.get_or_none(**statements)
        if user is not None:
            if verify_password(password, user.password):
                return user
        return None


class UserSettings(TortoiseModel):
    user = fields.OneToOneField("models.User", related_name="settings")
    wifi_load_only = fields.BooleanField(default=True)
    extra_authentication = fields.BooleanField(default=False)
    images_twice = fields.BooleanField(default=False)
