from tortoise import fields
from tortoise.exceptions import IntegrityError

import random
from typing import Optional

from .base import TortoiseModel
from .companies import Company
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

    @classmethod
    async def register(cls, fio: str, phone: str, email: str, password: str) -> Optional["User"]:
        try:
            new_user = await cls.create(
                fio=fio,
                phone=phone,
                email=email,
                password=hash_password(password)
            )
            await UserSettings.create(user=new_user)
            return new_user
        except IntegrityError:
            return None

    @classmethod
    async def login(cls, password: str, email: str | None = None, id: str | None = None) -> Optional["User"]:
        if email is None and id is None:
            return None
        if email is not None and id is not None:
            return None
        statements = {"email": email} if email is not None else {"id": id}
        user = await cls.get_or_none(**statements)
        if user is not None:
            if verify_password(password, user.password):
                return user
        return None

    async def get_settings(self) -> "UserSettings":
        return await self.settings.get()

    async def get_companies(self) -> list[Company]:
        return await self.companies.all()


class UserSettings(TortoiseModel):
    user = fields.OneToOneField("models.User", related_name="settings")
    wifi_load_only = fields.BooleanField(default=True)
    extra_authentication = fields.BooleanField(default=False)
    images_twice = fields.BooleanField(default=False)
