from pyrogram import filters
import asyncio
import pyfiglet 
from random import choice
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from pyrogram.handlers import MessageHandler
from PRINCEMUSIC import app

def create_figlet(text):
    fonts = pyfiglet.FigletFont.getFonts()
    font = choice(fonts)
    figlet_text = str(pyfiglet.figlet_format(text, font=font))
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("تغییر", callback_data="figlet"),
            InlineKeyboardButton("بستن", callback_data="close_reply")
        ]
    ])
    return figlet_text, keyboard

@app.on_message(filters.command("فیگلت"))
async def figlet_cmd(bot, message):
    global text
    try:
        text = message.text.split(' ', 1)[1]
    except IndexError:
        return await message.reply_text("مثال:\n\n`/فیگلت متن شما`")
        
    try:
        figlet_text, keyboard = create_figlet(text)
        await message.reply_text(
            f"متن فیگلت شما:\n<pre>{figlet_text}</pre>",
            quote=True,
            reply_markup=keyboard
        )
    except Exception as e:
        await message.reply_text(f"خطایی رخ داد: {str(e)}")

@app.on_callback_query(filters.regex("figlet"))
async def figlet_callback(client, query: CallbackQuery):
    try:
        figlet_text, keyboard = create_figlet(text)
        await query.message.edit_text(
            f"متن فیگلت شما:\n<pre>{figlet_text}</pre>",
            reply_markup=keyboard
        )
    except Exception as e:
        await query.message.reply_text(f"خطایی رخ داد: {str(e)}")

@app.on_callback_query(filters.regex("close_reply"))
async def close_reply(client, query: CallbackQuery):
    await query.message.delete()

__mod_name__ = "فیگلت"
