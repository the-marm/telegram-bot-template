from aiogram import Router

from . import start

routers_list: list[Router] = [
    start.router,
]

router = Router(name=__name__)
router.include_routers(*routers_list)
