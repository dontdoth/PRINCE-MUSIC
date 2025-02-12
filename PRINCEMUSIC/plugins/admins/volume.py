from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup

from PRINCEMUSIC import app
from PRINCEMUSIC.core.call import PRINCE
from PRINCEMUSIC.utils.database import is_active_chat
from PRINCEMUSIC.utils.decorators import AdminRightsCheck
from PRINCEMUSIC.utils.inline.play import volume_markup, stream_markup

@app.on_callback_query(filters.regex("^VOL"))
async def volume_markup_view(_, CallbackQuery):
    try:
        callback_data = CallbackQuery.data.strip()
        callback_request = callback_data.split(None, 1)[1]
        buttons = volume_markup(_, callback_request)
        await CallbackQuery.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        print(e)
        await CallbackQuery.answer("خطا!", show_alert=True)

@app.on_callback_query(filters.regex("^MainMenu"))
async def back_to_main_menu(_, CallbackQuery):
    try:
        callback_data = CallbackQuery.data.strip()
        chat_id = int(callback_data.split("|")[1])
        buttons = stream_markup(_, chat_id)
        await CallbackQuery.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        print(e)
        await CallbackQuery.answer("خطا!", show_alert=True)

@app.on_callback_query(filters.regex(pattern=r"^ADMIN"))
@AdminRightsCheck
async def admin_callbacks(_, CallbackQuery):
    try:
        command = CallbackQuery.data.split(None, 1)[1]
        chat_id = int(command.split("|")[1])
        action = command.split("|")[0]

        if action == "Volume":
            volume = int(command.split("|")[1])
            if not await is_active_chat(chat_id):
                return await CallbackQuery.answer("هیچ پخش فعالی وجود ندارد!", show_alert=True)
            
            if volume not in range(1, 201):
                return await CallbackQuery.answer("صدا باید بین 1 تا 200 باشد!", show_alert=True)
            
            try:
                await PRINCE.pytgcalls.change_volume_call(chat_id, volume)
                await CallbackQuery.answer(f"صدا به {volume}% تنظیم شد", show_alert=True)
            except:
                return await CallbackQuery.answer("خطا در تنظیم صدا!", show_alert=True)

        elif action == "CustomVolume":
            await CallbackQuery.answer("برای تنظیم صدای سفارشی از دستور /volume [1-200] استفاده کنید")

    except Exception as e:
        print(e)
        await CallbackQuery.answer("خطا!", show_alert=True)

@app.on_message(filters.command("volume") & filters.group)
@AdminRightsCheck
async def volume_cmd(_, message):
    if len(message.command) != 2:
        return await message.reply_text("استفاده نادرست!\n\nمثال: /volume 100")
        
    chat_id = message.chat.id
    if not await is_active_chat(chat_id):
        return await message.reply_text("هیچ پخش فعالی وجود ندارد!")
        
    try:
        volume = int(message.command[1])
    except:
        return await message.reply_text("لطفا یک عدد بین 1 تا 200 وارد کنید")
        
    if volume not in range(1, 201):
        return await message.reply_text("صدا باید بین 1 تا 200 باشد!")
        
    try:
        await PRINCE.pytgcalls.change_volume_call(chat_id, volume)
        await message.reply_text(f"🔊 صدا به {volume}% تنظیم شد")
    except:
        return await message.reply_text("خطا در تنظیم صدا!")
