import requests
from PRINCEMUSIC import app
from pyrogram import Client, filters

JOKE_API_ENDPOINT = 'https://open.wiki-api.ir/apis-1/4Jok'

@app.on_message(filters.command("hjoke"))
async def joke(_, message):
    try:
        response = requests.get(JOKE_API_ENDPOINT)
        if response.status_code == 200:
            jokes_data = response.json()
            # فرض می‌کنیم API یک لیست از جوک‌ها برمی‌گرداند
            if jokes_data and len(jokes_data) > 0:
                # انتخاب تصادفی یک جوک از لیست
                import random
                joke_text = random.choice(jokes_data)['text']  # یا هر کلید دیگری که API برمی‌گرداند
                await message.reply_text(joke_text)
            else:
                await message.reply_text("متاسفانه جوکی یافت نشد!")
        else:
            await message.reply_text("خطا در دریافت جوک. لطفا بعداً تلاش کنید.")
    except Exception as e:
        await message.reply_text(f"خطایی رخ داد: {str(e)}")
