import asyncio
import logging
import sys
import os
import pymysql
from dotenv import load_dotenv, dotenv_values
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
load_dotenv()

# Bot token can be obtained via https://t.me/BotFather
TOKEN=os.environ['TOKEN']
host=os.environ['DB_HOST']
user=os.environ['DB_USER']
passwd=os.environ['DB_PASSWD']
db=os.environ['DB_NAME']
ans="Hey"
try:
    # Attempt to establish a connection
    connection = pymysql.connect(host=host, port=3306, user=user, passwd=passwd, database=db)
    ans = "XConnected"
    connection.close()
    
except pymysql.Error as e:
    ans = "XError"
# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()

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
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@dp.message()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    await message.answer(ans)

async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


# Define the WSGI application
def application(environ, start_response):
    asyncio.run(main())
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b"Hello, World!"]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    application(None,None)