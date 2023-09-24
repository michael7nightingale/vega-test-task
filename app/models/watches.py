from uuid import uuid4

from fastapi import UploadFile
from tortoise import fields, Model

from .base import TortoiseModel
from ..core.config import get_app_settings
from ..services.files import filter_image_files, get_filename_extension


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
    finish_comment = fields.TextField(null=True)
    is_refused = fields.BooleanField(default=False)
    refuse_purpose = fields.TextField(null=True)
    note = fields.TextField(default="")
    contact_persons = fields.ManyToManyField("models.ContactPerson")

    async def refuse(self, refuse_purpose: str) -> None:
        if not self.is_finished:
            self.refuse_purpose = refuse_purpose
            self.is_refused = True
            self.is_finished = True
            await self.save()

    async def finish(self, finish_comment: str) -> None:
        if not self.is_finished:
            self.finish_comment = finish_comment
            self.is_finished = True
            await self.save()

    @classmethod
    def get_or_none(cls, *args, **kwargs):
        return (
            super()
            .get_or_none(*args, **kwargs)
            .prefetch_related("contact_persons")
        )

    @classmethod
    def get(cls, *args, **kwargs):
        return (
            super()
            .get(*args, **kwargs)
            .prefetch_related("contact_persons")
        )

    async def save_contacts(self, contact_persons: list[dict]):
        contact_persons_instances = []
        for contact_person in contact_persons:
            contact_persons_instances.append(
                await ContactPerson.create(**contact_person)
            )
        await self.contact_persons.add(*contact_persons_instances)
        return contact_persons_instances


class Task(TortoiseModel):
    title = fields.CharField(max_length=255)
    is_finished = fields.BooleanField(default=False)
    is_refused = fields.BooleanField(default=False)
    watch = fields.ForeignKeyField("models.Watch", related_name="tasks")

    async def refuse(self) -> None:
        if not self.is_finished:
            self.is_refused = True
            self.is_finished = True
            await self.save()

    async def finish(self) -> None:
        if not self.is_finished:
            self.is_finished = True
            await self.save()

    def __str__(self) -> str:
        return self.title


class Object(IsWatchMixin):
    watch = fields.ForeignKeyField("models.Watch", related_name="objects")
    title = fields.CharField(max_length=255)
    description = fields.CharField(max_length=255, default="")

    async def save_documents_images(self, files: list[UploadFile]) -> None:
        files = filter_image_files(files)
        settings = get_app_settings()
        for file in files:
            document_id = str(uuid4())
            filepath = settings.FILE_DIR + "documents/" + document_id + get_filename_extension(file.filename)
            document = await DocumentImage.create(
                id=document_id,
                object=self,
                image_path=filepath
            )
            with open(filepath, "wb") as file_save:
                file_save.write(await file.read())

    def __str__(self) -> str:
        return self.title


class ObjectPart(TortoiseModel):
    title = fields.CharField(max_length=255)
    description = fields.TextField(default="")
    object = fields.ForeignKeyField("models.Object", related_name="parts")

    async def save_images(self, files: list[UploadFile]) -> None:
        files = filter_image_files(files)
        settings = get_app_settings()
        for file in files:
            object_part_image_id = str(uuid4())
            filepath = settings.FILE_DIR + "objectparts/" + object_part_image_id + get_filename_extension(file.filename)
            object_part_image = await ObjectPartImage.create(
                id=object_part_image_id,
                object_part=self,
                image_path=filepath
            )
            with open(filepath, "wb") as file_save:
                file_save.write(await file.read())

    def __str__(self) -> str:
        return self.title


class ObjectPartImage(TortoiseModel):
    object_part = fields.ForeignKeyField("models.ObjectPart", related_name="images")
    image_path = fields.CharField(max_length=255)


class DocumentImage(TortoiseModel):
    object = fields.ForeignKeyField("models.Object", related_name="documents_images")
    image_path = fields.CharField(max_length=255)
