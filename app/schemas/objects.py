from pydantic import BaseModel


class ObjectCreateSchema(BaseModel):
    title: str
    description: str


class ObjectSchema(ObjectCreateSchema):
    id: str
    is_watched: str


class ObjectUpdateSchema(BaseModel):
    title: str | None = None
    description: str | None = None
