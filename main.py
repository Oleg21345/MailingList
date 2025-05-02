import asyncio
from database.model import create_tables, drop_tables
from bot.handlers.start_handler import main_context,bot
# from bot.dp_router import dp
from datetime import datetime

async def main():
    # await drop_tables()

    await create_tables()
    await main_context()



    # await dp.start_polling(bot, allowed_updates=["message", "callback_query"])

if __name__ == "__main__":

    asyncio.run(main())







