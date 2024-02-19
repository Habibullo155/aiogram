import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

bot = Bot(token='<Your_Token>')
dp = Dispatcher()


@dp.message(CommandStart())
async def start_command(message: types.Message) -> None:
    await message.answer('it\'s begin')


@dp.message()
async def say_hi(message: types.Message):
    text: str | None = message.text.lower()
    if text in ['привет', 'hi', 'hello', 'hey']:
        await message.answer('Hey, whats up')
    elif text in ['пока', 'покеда', 'bye']:
        await message.answer('by see you soon')
    else:
        message.answer(message.text)


async def main() -> None:
    await dp.start_polling(bot)


asyncio.run(main())
