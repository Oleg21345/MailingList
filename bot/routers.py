from bot.handlers.routers.router_start import router as router_start
from bot.handlers.change_time_handler import router as router_for_change
from aiogram import Dispatcher

dp = Dispatcher()


dp.include_router(router_start)
dp.include_router(router_for_change)









