import fastapi
from starlette.middleware.cors import CORSMiddleware

from core.config import envs
from routes.exceptions import apply_exception_handlers
from ugc_api.src.routes.v1.events import events

app = fastapi.FastAPI(
    title='UGC Service',
    description='Сервис отслеживания пользовательской активности онлайн-кинотеатра',
    swagger_ui_parameters={'docExpansion': 'none'}
)

apply_exception_handlers(app)

if not envs.app.cors_policy_enabled:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_methods=['*'],
        allow_headers=['*'],
        expose_headers=['Content-Disposition'],
        allow_credentials=True,
    )

app.include_router(events, prefix='v1/events', tags=['Events'])
