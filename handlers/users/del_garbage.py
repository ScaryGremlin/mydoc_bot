from aiogram import types
from aiogram.dispatcher.filters import ContentTypeFilter

from loader import dispatcher


@dispatcher.message_handler(ContentTypeFilter(types.ContentType.STICKER))
@dispatcher.message_handler(ContentTypeFilter(types.ContentType.ANY))
async def del_garbage_messages(message: types.Message):
    await message.delete()
