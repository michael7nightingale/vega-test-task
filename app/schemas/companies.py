from pydantic import BaseModel


class CompanySchema(BaseModel):
    city: str
    title: str
    juridical_responsibility: str
