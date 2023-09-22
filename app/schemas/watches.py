from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class ContactPersonSchema(BaseModel):
    fio: str
    phone: str = Field(max_length=10, min_length=10)

    @field_validator("fio")
    @classmethod
    def validate_fio(cls, value: str):
        try:
            surname, name, father_name = value.split()
        except IndexError:
            raise ValueError("Incorrect fio format!")
        else:
            return value


class ContactPersonUpdateSchema(ContactPersonSchema):
    fio: str | None = None
    phone: str | None = None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str):
        if len(value) != 10:
            raise ValueError("Phone number must be length of 10!")
        return value


class WatchSchema(BaseModel):
    address: str
    time_start: datetime
    time_finished: datetime | None = None
    is_watched: bool
    is_finished: bool
    is_refused: bool
    refuse_purpose: str | None = None
    note: str
    contact_persons: list[ContactPersonSchema] = Field(default_factory=list)


class WatchUpdateSchema(BaseModel):
    address: str | None = None
    time_start: datetime | None = None
    time_finished: datetime | None = None
    note: str | None = None


class WatchRefuseSchema(BaseModel):
    refuse_purpose: str


class WatchFinishSchema(BaseModel):
    finish_comment: str


class TaskSchema(BaseModel):
    title: str
    is_finished: bool
    is_refused: bool


class TaskUpdateSchema(BaseModel):
    title: str | None = None
    is_finished: bool | None = None
    is_refused: bool | None = None


class ObjectSchema(BaseModel):
    title: str
    description: str
    is_watched: str


class ObjectUpdateSchema(BaseModel):
    title: str | None = None
    description: str | None = None
