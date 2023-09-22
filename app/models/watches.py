from tortoise import fields, Model

from .base import TortoiseModel


class IsWatchMixin(TortoiseModel):
    is_watched = fields.BooleanField(default=False)

    class Meta:
        abstract = True

    async def watch(self) -> None:
        self.is_watched = True
        await self.save()


class ContactPerson(TortoiseModel):
    fio = fields.CharField(max_length=255)
    phone = fields.CharField(max_length=10)

    def __str__(self) -> str:
        return self.fio


class Watch(IsWatchMixin):
    user = fields.ForeignKeyField("models.User", related_name="watches")
    address = fields.CharField(max_length=255)
    time_start = fields.DatetimeField()
    time_finished = fields.DatetimeField(null=True)
    is_finished = fields.BooleanField(default=False)
    finish_comment = fields.CharField(null=True)
    is_refused = fields.BooleanField(default=False)
    refuse_purpose = fields.TextField(null=True)
    note = fields.TextField(default="")
    contact_persons = fields.ManyToManyField("models.ContactPerson")

    async def refuse(self, refuse_purpose: str) -> None:
        self.refuse_purpose = refuse_purpose
        self.is_refused = True
        self.is_finished = True
        await self.save()

    async def finish(self, finish_comment: str) -> None:
        self.finish_comment = finish_comment
        self.is_finished = True
        await self.save()


class Task(TortoiseModel):
    title = fields.CharField(max_length=255)
    is_finished = fields.BooleanField(default=False)
    is_refused = fields.BooleanField(default=False)
    watch = fields.ForeignKeyField("models.Watch", related_name="tasks")

    async def refuse(self, refuse_purpose: str) -> None:
        self.is_refused = True
        self.is_finished = True
        await self.save()

    def __str__(self) -> str:
        return self.title


class Object(IsWatchMixin):
    watch = fields.ForeignKeyField("models.Watch", related_name="objects")
    title = fields.CharField(max_length=255)
    description = fields.CharField(max_length=255, default="")

    def __str__(self) -> str:
        return self.title
