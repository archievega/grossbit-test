from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from cash_machine.config import Settings
from cash_machine.repositories.general import Repository
from cash_machine.database import get_async_session


def create_app(settings: Settings):
    app = FastAPI(
        title="Grossbit",
        root_path=f"{settings.api.prefix}{settings.api.v1.prefix}",
        default_response_class=ORJSONResponse,
        routes=[
            Mount(
                "/cash_machine/media",
                app=StaticFiles(directory="/media"),
                name="media",
            ),
        ],
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.dependency_overrides[Repository] = Repository(get_async_session)

    return app
