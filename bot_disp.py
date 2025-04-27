import asyncio
import logging
import sys
from datetime import datetime, timedelta
from idlelib.window import add_windows_to_menu
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from utils.utils import last_day_of_month, generate_button

load_dotenv(dotenv_path='config/config.env')
TOKEN = getenv("BOT_TOKEN")

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()


def create_kb(message: Message):
    kb_list = [
        [KeyboardButton(text=f"Hello, {html.bold(message.from_user.full_name)}!")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    # генерировать кнопки с часами. после нажатия убирать кнопку. плюс кнопка назад. чтобы вернутся к датам

    await message.answer('В какое время на следующей неделе ты готов собраться?',
                         reply_markup=generate_button('text'))


@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    # TODO: добавить бд с пользователями датами и временем
    if message.text == 'Готово':
        await message.answer('Планы построены', reply_markup=ReplyKeyboardRemove())
        # TODO: кнопка для начала планирования
        return

    if '.' in message.text and len(message.text.split('.')) == 2:
        if (int(message.text.split('.')[0]) > last_day_of_month(datetime.now())
                or 0 > int(message.text.split('.')[1]) > 12):
            await message.answer('Некорректная дата, воспользуйся кнопками')
            return
        message_type = 'date'
    elif ':' in message.text and len(message.text.split(':')) == 2:
        if 0 >= int(message.text.split(':')[0]) > 24 or 0 >= int(message.text.split(':')[1]) > 60:
            await message.answer('Некорректное время, воспользуйся кнопками')
            return
        message_type = 'time'
    else:
        message_type = 'text'

    # menu_button = generate_button(message_type)

    await message.answer(text='text example', reply_markup=generate_button(message_type))


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
