from aiogram import Router

from . import errors

routers_list: list[Router] = [
    errors.router,
]

router = Router(name=__name__)
router.include_routers(*routers_list)
