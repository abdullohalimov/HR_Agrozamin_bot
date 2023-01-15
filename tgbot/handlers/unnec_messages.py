from aiogram import Dispatcher
from aiogram.types import Message, ContentType

async def unnecessary_messages(message: Message):
    await message.delete()
    print('message unneccesarily')


def register_unnec_messages(dp: Dispatcher):
    dp.register_message_handler(unnecessary_messages, content_types=ContentType.all(), state="*")
