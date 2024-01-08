import asyncio
import logging.handlers

from aiogram.types import ChatJoinRequest, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Bot, Dispatcher, F


BOT_TOKEN = "6624981848:AAFfhb6HBsTA6s9-nNqBnQgcFvJ0dVLgaMY"
CHANNEL_ID = -1002051048969


async def approve_request(chat_join: ChatJoinRequest, bot: Bot):
    msg = "*🎉Поздравляю*\nНажми чтобы получить бесплатный пробив👇"
    hash = f"dOSd4mSMrQ7Djua6{chat_join.from_user.id}6UaMNQp6b5Wxp73Mn"
    kb = [
        [InlineKeyboardButton(text="Получить бонус",
                              url=f"https://unmasking.net/get-bonus/{hash}")]
    ]
    await bot.send_message(chat_id=chat_join.from_user.id, text=msg,
                           reply_markup=InlineKeyboardMarkup(inline_keyboard=kb), parse_mode='MarkdownV2')
    await chat_join.approve()


async def start():
    bot: Bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.chat_join_request.register(approve_request, F.chat.id==CHANNEL_ID)

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as x:
        exit()


if __name__ == "__main__":
    asyncio.run(start())
