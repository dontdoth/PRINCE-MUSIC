from PRINCEMUSIC import app 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup 
from pyrogram import filters 
import requests

API_URL = "https://sugoi-api.vercel.app/search"

@app.on_message(filters.command("جستجو"))
async def bing_search(_, message):
    if len(message.command) == 1:
        return await message.reply_text("لطفا کلمه مورد نظر برای جستجو را وارد کنید.")

    try:
        keyword = " ".join(message.command[1:])
        response = requests.get(API_URL, params={"keyword": keyword})
        
        if not response.ok:
            return await message.reply_text("متأسفانه مشکلی در جستجو پیش آمد.")

        results = response.json()
        if not results:
            return await message.reply_text("نتیجه‌ای یافت نشد.")

        keyboard = []
        for i, result in enumerate(results[:5], start=1):
            title = result.get("title", "بدون عنوان")
            link = result.get("link", "")
            keyboard.append([InlineKeyboardButton(f"{i}. {title[:30]}...", url=link)])
            
        reply_markup = InlineKeyboardMarkup(keyboard)
        await message.reply_text(
            f"🔎 نتایج جستجو برای: **{keyword}**\n\n"
            "برای مشاهده نتایج روی لینک‌ها کلیک کنید:",
            reply_markup=reply_markup
        )

    except Exception as e:
        await message.reply_text(f"خطایی رخ داد: {str(e)}")
