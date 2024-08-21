import uvicorn
from fastapi import FastAPI

from cash_machine.config import settings

from cash_machine.routers import router as api_router
from cash_machine.app import create_app

main_app: FastAPI = create_app(settings=settings)

main_app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
