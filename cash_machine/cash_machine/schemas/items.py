from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    title: str
    price: int = Field(gt=0, lt=2147483647)


class ItemGetResponse(ItemCreate):
    id: int
    


class ItemCreateResponse(ItemGetResponse):
    pass




