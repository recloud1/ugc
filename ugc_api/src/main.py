import fastapi
from core.config import envs
from core.log_config import set_logging
from routes.exceptions import apply_exception_handlers
from routes.v1.bookmarks import bookmarks
from routes.v1.events import events
from routes.v1.likes import likes
from routes.v1.reviews import reviews
from starlette.middleware.cors import CORSMiddleware

app = fastapi.FastAPI(
    title="UGC Service",
    description="Сервис отслеживания пользовательской активности онлайн-кинотеатра",
    swagger_ui_parameters={"docExpansion": "none"},
)

set_logging(
    level=envs.log_level,
    sentry_url=envs.logging.sentry_url,
    environment=envs.app.environment,
    app=app,
)

apply_exception_handlers(app)

if not envs.app.cors_policy_enabled:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Disposition"],
        allow_credentials=True,
    )

app.include_router(events, prefix="/v1/events", tags=["Events"])
app.include_router(bookmarks, prefix="/v1/bookmarks", tags=["Bookmarks"])
app.include_router(likes, prefix="/v1/reviews", tags=["Likes"])
app.include_router(reviews, prefix="/v1/reviews", tags=["Reviews"])
