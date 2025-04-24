from aiogram import Bot, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config.config import BOT_TOKEN
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from aiogram import F
from aiogram.filters.command import Command
import asyncio
from database.method_database import MetodSQL
from bot.routers import dp
from bot.handlers.routers.router_start import router
import config.config as config
from pytz import UTC


bot = Bot(token=BOT_TOKEN)
scheduler = AsyncIOScheduler()


register_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Зарегистрироваться", callback_data="register")]
])

global webtime

@router.message(Command("start"))
async def on_start(message: types.Message):
    global webtime
    webtim = config.WEBINAR_TIME_KYIV
    webtime = webtim.astimezone(UTC)
    is_registered = await MetodSQL.is_user_registered(message.from_user.id)
    if is_registered:
        text = (
            "Привет! 👋\n"
            "Ты уже зарегистрирован(а) на вебинар. Напоминаю, что:\n\n"
            "📅 На вебинаре «Автоматизируй рутину с ИИ» я покажу, как использовать искусственный интеллект для автоматизации процессов и личных задач.\n\n"
            f"🕒 Вебинар пройдёт сегодня:\n"
            f"{config.WEBINAR_TIME_KYIV.strftime('%d.%m.%Y в %H:%M')} Варшава | "
            f"{(config.WEBINAR_TIME_KYIV + timedelta(hours=1)).strftime('%H:%M')} Киев.\n\n"
            "🔧 Никакой лишней теории — только практические инструменты, которые уже сегодня помогут сэкономить время и ресурсы. Ты узнаешь:\n\n"
            "✅ Как автоматизировать рутинные задачи без программирования\n"
            "✅ Какие ИИ-инструменты помогут в работе и жизни\n"
            "✅ Реальные кейсы, которые я ежедневно использую в своих компаниях\n\n"
            "До встречи на вебинаре! 🔥"
        )
        await message.answer(text)
        return

    welcome_text = (
        "Привет! 👋\n"
        "На вебинаре «Автоматизируй рутину с ИИ» я покажу, как использовать искусственный интеллект для автоматизации процессов и личных задач.\n\n"
        f"Вебинар пройдёт сегодня:\n"
        f"{config.WEBINAR_TIME_KYIV.strftime('%d.%m.%Y в %H:%M')} Варшава | "
        f"{(config.WEBINAR_TIME_KYIV + timedelta(hours=1)).strftime('%H:%M')} Киев.\n\n"
        "Никакой лишней теории — только практические инструменты, которые уже сегодня помогут сэкономить время и ресурсы. Вы узнаете:\n\n"
        "✅ Как автоматизировать рутинные задачи без программирования\n"
        "✅ Какие ИИ-инструменты помогут в работе и жизни\n"
        "✅ Реальные кейсы, которые я ежедневно использую в своих компаниях\n\n"
        "Нажмите «Зарегистрироваться» и получите подарок 🎁 — 30-минутный бесплатный урок:\n"
        "«Как автоматизировать работу юриста и обработку документов с помощью ИИ»"
    )
    await message.answer(welcome_text, reply_markup=register_kb)


@router.callback_query(F.data == "register")
async def on_register(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    username = callback_query.from_user.username
    at = datetime.now(timezone.utc)

    await MetodSQL.add(user_id, username, at=at)

    await schedule_reminders(user_id)

    await callback_query.message.answer("✅ Вы зарегистрированы на вебинар! Мы напомним вам о начале.")
    await callback_query.answer()


from datetime import datetime, timedelta, timezone

async def schedule_reminders(user_id: int):
    global webtime

    now = datetime.now(timezone.utc)

    WEBINAR_TIME = webtime

    reminder_30min = WEBINAR_TIME - timedelta(minutes=30)
    reminder_30min = reminder_30min.replace(tzinfo=timezone.utc)
    if reminder_30min > now:
        scheduler.add_job(
            send_reminder,
            DateTrigger(reminder_30min),
            args=(user_id, "⏰ Напоминаем, что через 30 минут начнется вебинар «Автоматизируй рутину с ИИ»!"),
        )

    reminder_5min = WEBINAR_TIME - timedelta(minutes=5)
    reminder_5min = reminder_5min.replace(tzinfo=timezone.utc)

    if reminder_5min > now:
        scheduler.add_job(
            send_reminder,
            DateTrigger(reminder_5min),
            args=(user_id, "🔔 Вебинар начнется через 5 минут! Приготовьтесь!"),
        )

    WEBINAR_TIME = WEBINAR_TIME.replace(tzinfo=timezone.utc)
    if WEBINAR_TIME > now:
        scheduler.add_job(
            send_reminder,
            DateTrigger(WEBINAR_TIME),
            args=(user_id, "🚀 Вебинар начинается прямо сейчас! Присоединяйтесь!"),
        )

    reminder_90min_after = WEBINAR_TIME + timedelta(minutes=90)
    reminder_90min_after = reminder_90min_after.replace(tzinfo=timezone.utc)
    if reminder_90min_after > now:
        scheduler.add_job(
            send_reminder,
            DateTrigger(reminder_90min_after),
            args=(user_id, "📚 Спасибо за участие в вебинаре! Вот материалы и запись..."),
        )

async def send_reminder(user_id: int, message: str):
    try:
        await bot.send_message(user_id, message)
    except Exception as e:
        print(f"Не удалось отправить напоминание пользователю {user_id}: {e}")


async def on_startup():
    scheduler.start()

    users = await MetodSQL.get_all_users()
    for user in users:
        await schedule_reminders(user['user_id'])


async def main_context():
    await on_startup()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main_context())
























































# from aiogram import Bot, types
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from config.config import BOT_TOKEN, WEBINAR_TIME
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from apscheduler.triggers.date import DateTrigger
# from aiogram import F
# from aiogram.filters.command import Command, Message
# import asyncio
# from database.method_database import MetodSQL
# from bot.routers import dp
# from bot.handlers.routers.router_start import router
# import config.config as config
# import pytz
#
#
# bot = Bot(token=BOT_TOKEN)
# scheduler = AsyncIOScheduler()
#
#
# register_kb = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text="Зарегистрироваться", callback_data="register")]
# ])
#
#
# @router.message(Command("start"))
# async def on_start(message: types.Message):
#     welcome_text = (
#         "Привет! 👋\n"
#         "На вебинаре «Автоматизируй рутину с ИИ» я покажу, как использовать искусственный интеллект для автоматизации процессов и личных задач.\n\n"
#         f"Вебинар пройдёт сегодня:\n"
#         f"{config.WEBINAR_TIME.strftime('%d.%m.%Y в %H:%M')} Варшава | "
#         f"{(config.WEBINAR_TIME + timedelta(hours=1)).strftime('%H:%M')} Киев.\n\n"
#         "Никакой лишней теории — только практические инструменты, которые уже сегодня помогут сэкономить время и ресурсы. Вы узнаете:\n\n"
#         "✅ Как автоматизировать рутинные задачи без программирования\n"
#         "✅ Какие ИИ-инструменты помогут в работе и жизни\n"
#         "✅ Реальные кейсы, которые я ежедневно использую в своих компаниях\n\n"
#         "Нажмите «Зарегистрироваться» и получите подарок 🎁 — 30-минутный бесплатный урок:\n"
#         "«Как автоматизировать работу юриста и обработку документов с помощью ИИ»"
#     )
#     await message.answer(welcome_text, reply_markup=register_kb)
#
# @router.callback_query(F.data == "register")
# async def on_register(callback_query: types.CallbackQuery):
#     user_id = callback_query.from_user.id
#     username = callback_query.from_user.username
#     at = datetime.now(timezone.utc)
#
#     await MetodSQL.add(user_id, username, at=at)
#
#     await schedule_reminders(user_id)
#
#     await callback_query.message.answer("✅ Вы зарегистрированы на вебинар! Мы напомним вам о начале.")
#     await callback_query.answer()
#
#
# from datetime import datetime, timedelta, timezone
#
# async def schedule_reminders(user_id: int):
#     now = datetime.now(timezone.utc)
#     from config.config import WEBINAR_TIME
#
#     reminder_30min = WEBINAR_TIME - timedelta(minutes=30)
#     reminder_30min = reminder_30min.replace(tzinfo=timezone.utc)
#     print(f"rem30 {reminder_30min}")
#     if reminder_30min > now:
#         scheduler.add_job(
#             send_reminder,
#             DateTrigger(reminder_30min),
#             args=(user_id, "⏰ Напоминаем, что через 30 минут начнется вебинар «Автоматизируй рутину с ИИ»!"),
#         )
#
#     reminder_5min = WEBINAR_TIME - timedelta(minutes=5)
#     reminder_5min = reminder_5min.replace(tzinfo=timezone.utc)
#     print(f"rem5 {reminder_5min}")
#
#     if reminder_5min > now:
#         scheduler.add_job(
#             send_reminder,
#             DateTrigger(reminder_5min),
#             args=(user_id, "🔔 Вебинар начнется через 5 минут! Приготовьтесь!"),
#         )
#
#     WEBINAR_TIME = WEBINAR_TIME.replace(tzinfo=timezone.utc)
#     if WEBINAR_TIME > now:
#         scheduler.add_job(
#             send_reminder,
#             DateTrigger(WEBINAR_TIME),
#             args=(user_id, "🚀 Вебинар начинается прямо сейчас! Присоединяйтесь!"),
#         )
#
#     reminder_90min_after = WEBINAR_TIME + timedelta(minutes=90)
#     reminder_90min_after = reminder_90min_after.replace(tzinfo=timezone.utc)
#     if reminder_90min_after > now:
#         scheduler.add_job(
#             send_reminder,
#             DateTrigger(reminder_90min_after),
#             args=(user_id, "📚 Спасибо за участие в вебинаре! Вот материалы и запись..."),
#         )
#
# async def send_reminder(user_id: int, message: str):
#     try:
#         await bot.send_message(user_id, message)
#     except Exception as e:
#         print(f"Не удалось отправить напоминание пользователю {user_id}: {e}")
#
#
# async def on_startup():
#     scheduler.start()
#
#     users = await MetodSQL.get_all_users()
#     for user in users:
#         await schedule_reminders(user['user_id'])
#
#
# async def main_context():
#     await on_startup()
#     await dp.start_polling(bot)
#
#
# if __name__ == "__main__":
#     asyncio.run(main_context())


























# from aiogram import Bot, types
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from config.config import BOT_TOKEN, WEBINAR_TIME
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from apscheduler.triggers.date import DateTrigger
# from aiogram import F
# from aiogram.filters.command import Command, Message
# import asyncio
# from database.method_database import MetodSQL
# from bot.routers import dp
# from bot.handlers.routers.router_start import router
# import config.config as config
# import pytz
#
#
# bot = Bot(token=BOT_TOKEN)
# scheduler = AsyncIOScheduler()
#
#
# register_kb = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text="Зарегистрироваться", callback_data="register")]
# ])
#
#
# @router.message(Command("start"))
# async def on_start(message: types.Message):
#     welcome_text = (
#         "Привет! 👋\n"
#         "На вебинаре «Автоматизируй рутину с ИИ» я покажу, как использовать искусственный интеллект для автоматизации процессов и личных задач.\n\n"
#         f"Вебинар пройдёт сегодня:\n"
#         f"{config.WEBINAR_TIME.strftime('%d.%m.%Y в %H:%M')} Варшава | "
#         f"{(config.WEBINAR_TIME + timedelta(hours=1)).strftime('%H:%M')} Киев.\n\n"
#         "Никакой лишней теории — только практические инструменты, которые уже сегодня помогут сэкономить время и ресурсы. Вы узнаете:\n\n"
#         "✅ Как автоматизировать рутинные задачи без программирования\n"
#         "✅ Какие ИИ-инструменты помогут в работе и жизни\n"
#         "✅ Реальные кейсы, которые я ежедневно использую в своих компаниях\n\n"
#         "Нажмите «Зарегистрироваться» и получите подарок 🎁 — 30-минутный бесплатный урок:\n"
#         "«Как автоматизировать работу юриста и обработку документов с помощью ИИ»"
#     )
#     await message.answer(welcome_text, reply_markup=register_kb)
#
# @router.callback_query(F.data == "register")
# async def on_register(callback_query: types.CallbackQuery):
#     user_id = callback_query.from_user.id
#     username = callback_query.from_user.username
#     at = datetime.now(timezone.utc)
#
#     await MetodSQL.add(user_id, username, at=at)
#
#     await schedule_reminders(user_id)
#
#     await callback_query.message.answer("✅ Вы зарегистрированы на вебинар! Мы напомним вам о начале.")
#     await callback_query.answer()
#
#
# from datetime import datetime, timedelta, timezone
#
#
# async def schedule_reminders(user_id: int):
#     kyiv_tz = pytz.timezone("Europe/Kyiv")
#
#     now = datetime.now(kyiv_tz)
#     from config.config import WEBINAR_TIME
#
#     reminder_30min = WEBINAR_TIME - timedelta(minutes=30)
#     print(f"30minut  {reminder_30min}")
#     reminder_30min = reminder_30min.replace(tzinfo=kyiv_tz)
#     if reminder_30min > now:
#         scheduler.add_job(
#             send_reminder,
#             DateTrigger(reminder_30min),
#             args=(user_id, "⏰ Напоминаем, что через 30 минут начнется вебинар «Автоматизируй рутину с ИИ»!"),
#         )
#
#     reminder_5min = WEBINAR_TIME - timedelta(minutes=5)
#     print(f"5 minut {reminder_5min}")
#     reminder_5min = reminder_5min.replace(tzinfo=kyiv_tz)
#     if reminder_5min > now:
#         scheduler.add_job(
#             send_reminder,
#             DateTrigger(reminder_5min),
#             args=(user_id, "🔔 Вебинар начнется через 5 минут! Приготовьтесь!"),
#         )
#
#     WEBINAR_TIME = WEBINAR_TIME.replace(tzinfo=kyiv_tz)
#     if WEBINAR_TIME > now:
#         scheduler.add_job(
#             send_reminder,
#             DateTrigger(WEBINAR_TIME),
#             args=(user_id, "🚀 Вебинар начинается прямо сейчас! Присоединяйтесь!"),
#         )
#
#     reminder_90min_after = WEBINAR_TIME + timedelta(minutes=90)
#     print(reminder_5min)
#     reminder_90min_after = reminder_90min_after.replace(tzinfo=kyiv_tz)
#
#     if reminder_90min_after > now:
#         scheduler.add_job(
#             send_reminder,
#             DateTrigger(reminder_90min_after),
#             args=(user_id, "📚 Спасибо за участие в вебинаре! Вот материалы и запись..."),
#         )
#
# async def send_reminder(user_id: int, message: str):
#     try:
#         await bot.send_message(user_id, message)
#     except Exception as e:
#         print(f"Не удалось отправить напоминание пользователю {user_id}: {e}")
#
#
# async def on_startup():
#     scheduler.start()
#
#     users = await MetodSQL.get_all_users()
#     for user in users:
#         await schedule_reminders(user['user_id'])
#
#
# async def main_context():
#     await on_startup()
#     await dp.start_polling(bot)
#
#
# if __name__ == "__main__":
#     asyncio.run(main_context())
