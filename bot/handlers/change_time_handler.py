from aiogram import Router
from aiogram.filters import Command
from aiogram import  F
from aiogram.types import Message
from datetime import datetime
import config.config as config
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from pytz import timezone

router = Router()

class WebinarStates(StatesGroup):
    waiting_for_time = State()


@router.message(Command("admin_command"))
async def ask_for_new_time(message: Message, state: FSMContext):
    await message.answer("Введите новое время вебинара, сейчас: `дд.мм.рррр гг:хх`\nПример: `25.04.2025 18:30`")
    await state.set_state(WebinarStates.waiting_for_time)

@router.message(WebinarStates.waiting_for_time, F.text.regexp(r"\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}"))
async def set_new_time(message: Message, state: FSMContext):
    try:
        kyiv_tz = timezone("Europe/Kyiv")
        utc_tz = timezone("UTC")

        naive_dt = datetime.strptime(message.text, "%d.%m.%Y %H:%M")

        kyiv_dt = kyiv_tz.localize(naive_dt)

        utc_dt = kyiv_dt.astimezone(utc_tz)

        config.WEBINAR_TIME_KYIV = kyiv_dt
        config.WEBINAR_TIME_UTC = utc_dt

        await message.answer(
            f"✅ Время вебинара было изменено на {kyiv_dt.strftime('%d.%m.%Y %H:%M')} (Kyiv)\n"
        )
        await state.clear()

    except ValueError:
        await message.answer("❌ Неправильний формат. Попробуйте еще раз.")
