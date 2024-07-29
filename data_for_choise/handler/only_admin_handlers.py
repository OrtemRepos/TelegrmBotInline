from aiogram import Router
from ..handler import admin_handlers, edit_handlers, common, delete_handlers
from ..middleware import OnlyAdminMiddleware

router = Router()
router.message.middleware(OnlyAdminMiddleware())
router.include_routers(common.router, delete_handlers.router, admin_handlers.router, edit_handlers.router)
