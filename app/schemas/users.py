from pydantic import BaseModel, FieldValidationInfo, field_validator, EmailStr, Field

from typing import Any


class BaseUserSchema(BaseModel):
    fio: str
    email: EmailStr
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


class PasswordConfirmationMixin(BaseModel):
    password: str
    confirm_password: str

    @field_validator("confirm_password")
    @classmethod
    def validate_confirm_password(cls, value: str, info: FieldValidationInfo):
        if info.data['password'] != value:
            raise ValueError("Password and confirmation do not match!")
        return value


class UserSchema(BaseUserSchema):
    id: str


class LoginUserSchema(BaseModel):
    login: str
    password: str

    id: str | None = None
    email: EmailStr | None = None

    def model_post_init(self, __context: Any) -> None:
        if self.login.isnumeric():
            self.id = self.login
            self.email = None
        else:
            self.email = self.login
            self.id = None


class RegisterUserSchema(PasswordConfirmationMixin, BaseUserSchema):
    pass


class UpdateUserSchema(PasswordConfirmationMixin, BaseModel):
    fio: str | None = None
    email: EmailStr | None = None
    phone: str = None

    password: str | None = None
    confirm_password: str | None = None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str):
        if len(value) != 10:
            raise ValueError("Phone number must be length of 10!")
        return value


class UserSettingsSchema(BaseModel):
    wifi_load_only: bool
    extra_authentication: bool
    images_twice: bool


class UserSettingsUpdateSchema(BaseModel):
    wifi_load_only: bool | None = None
    extra_authentication: bool | None = None
    images_twice: bool | None = None
