__all__ = ("router",)

from aiogram import Router


from .group_handlers import router as group_router
from .schedule_handlers import router as schedule_router
from .settings_handlers import router as settings_router
from .common_handlers import router as common_router


router = Router(name=__name__)

router.include_routers(
    settings_router,
    group_router,
    schedule_router,
    # end
    common_router,
)
