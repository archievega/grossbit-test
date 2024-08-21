from pydantic import BaseModel, ConfigDict, Field


class ItemCreate(BaseModel):
    title: str
    price: float = Field(gt=0, lt=2147483647)


class ItemGetResponse(ItemCreate):
    model_config: ConfigDict = ConfigDict(from_attributes=True)
    id: int


class ItemCreateResponse(ItemGetResponse):
    pass
