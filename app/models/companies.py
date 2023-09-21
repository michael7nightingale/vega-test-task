from tortoise import fields

from .base import TortoiseModel


class Company(TortoiseModel):
    city = fields.CharField(max_length=30)
    title = fields.CharField(max_length=50, unique=True, index=True)
    juridical_responsibility = fields.CharField(max_length=3, default="ООО")
