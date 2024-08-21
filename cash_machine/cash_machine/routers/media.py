from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os


router = APIRouter(prefix="/media")


@router.get("/{check_id}")
async def get_check_pdf(check_id: str):
    file_path = f"media/{check_id}.pdf"
    print(file_path)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="PDF file not found")
    return FileResponse(path=file_path, media_type="application/pdf")
