from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from cash_machine.repositories import Repository, get_repository
from cash_machine.schemas.items import ItemCreate, ItemCreateResponse, ItemGetResponse

router = APIRouter(prefix="/items")


@router.post("/", response_model=ItemCreateResponse)
async def create_item(item_data: ItemCreate, repository: Annotated[Repository, Depends(get_repository)]):
    item = await repository.items.create(**item_data.model_dump())
    return item


@router.get("/{item_id}", response_model=ItemGetResponse)
async def get_item(item_id: int, repository: Annotated[Repository, Depends(get_repository)]):
    item = await repository.items.get(item_id)
    if not item:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.get("/", response_model=list[ItemGetResponse])
async def get_items(repository: Annotated[Repository, Depends(get_repository)]):
    items = await repository.items.get_all()
    print(type(items))
    return items