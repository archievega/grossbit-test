from pydantic import BaseModel


class CheckCreate(BaseModel):
    items: list[int]
