from pydantic import BaseModel


class TaskCreateSchema(BaseModel):
    title: str


class TaskSchema(BaseModel):
    id: str
    title: str
    is_finished: bool
    is_refused: bool


class TaskUpdateSchema(BaseModel):
    title: str | None = None
    is_finished: bool | None = None
    is_refused: bool | None = None
