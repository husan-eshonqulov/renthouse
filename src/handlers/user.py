from aiogram.types import Message

from messages import MessageService


async def start_handler(msg: Message, messages: MessageService):
    await msg.answer(f"{messages.start_message()}!")
