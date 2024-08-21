from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, status, Response
from collections import defaultdict
from typing import Annotated
from cash_machine.repositories import Repository, get_repository
from cash_machine.schemas.checks import CheckCreate
from cash_machine.schemas.items import ItemGetResponse
from cash_machine.check_generation import render_pdf_check
from datetime import datetime
from cash_machine.config import settings
import qrcode
from io import BytesIO


router = APIRouter(prefix="/cash_machine")


async def fetch_items(data: CheckCreate, repository: Repository) -> list[dict]:
    items = []
    for item_id in data.items:
        item = await repository.items.get(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item #{item_id} not found",
            )
        items.append(ItemGetResponse.model_validate(item).model_dump())
    return items


def count_items(items: list[dict]) -> list[dict]:
    item_counter = defaultdict(lambda: {"quantity": 0, "total": 0, "title": ""})
    for item in items:
        id = item["id"]
        item_counter[id]["quantity"] += 1
        item_counter[id]["total"] += item["price"]
        item_counter[id]["title"] = item["title"]
        if "price" not in item_counter[id]:
            item_counter[id]["price"] = item["price"]
    return list(item_counter.values())


def generate_template_data(items: list[dict]) -> dict:
    now = datetime.now()
    date_str = now.strftime("%d.%m.%Y")
    time_str = now.strftime("%H:%M")
    total_price = sum(item["total"] for item in items)
    return {
        "date": date_str,
        "time": time_str,
        "items": items,
        "total_price": f"{total_price}",
    }


def create_qr_code(url: str) -> BytesIO:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    img_buffer = BytesIO()
    img.save(img_buffer)
    img_buffer.seek(0)
    return img_buffer


def get_pdf_url(id: str) -> str:
    return f"http://{settings.run.public_url}/media/{id}"


@router.post("/")
async def generate_qr(
    data: CheckCreate, repository: Annotated[Repository, Depends(get_repository)]
):
    items = await fetch_items(data, repository)
    formatted_items = count_items(items)
    template_data = generate_template_data(formatted_items)

    check_id = str(uuid4())
    render_pdf_check(check_id, template_data)

    pdf_url = get_pdf_url(check_id)
    print(pdf_url)
    img_buffer = create_qr_code(pdf_url)

    return Response(content=img_buffer.getvalue(), media_type="image/png")
