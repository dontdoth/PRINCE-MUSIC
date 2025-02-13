from pyrogram import filters
import random
from PRINCEMUSIC import YouTube, app
from PRINCEMUSIC.utils.channelplay import get_channeplayCB
from PRINCEMUSIC.utils.decorators.language import languageCB
from PRINCEMUSIC.utils.stream.stream import stream
from config import BANNED_USERS

# لیست کانال‌های تلویزیونی (به عنوان مثال)
TV_CHANNELS = {
    "pmc": "https://hls.pmchd.live/hls/stream.m3u8",
    "manoto": "https://live.manototv.com/live/manoto_tv.m3u8",
    "bbc": "https://bbcpersian-live.bbcfmt.hs.llnwd.net/stream.m3u8",
    # کانال‌های بیشتر را اینجا اضافه کنید
}

@app.on_callback_query(filters.regex("TVStream") & ~BANNED_USERS)
@languageCB
async def play_tv_stream(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    channel_id, user_id, mode, cplay, fplay = callback_request.split("|")
    
    if CallbackQuery.from_user.id != int(user_id):
        try:
            return await CallbackQuery.answer("این دکمه برای شما نیست!", show_alert=True)
        except:
            return
            
    try:
        chat_id, channel = await get_channeplayCB(_, cplay, CallbackQuery)
    except:
        return
        
    video = True if mode == "v" else None
    user_name = CallbackQuery.from_user.first_name
    await CallbackQuery.message.delete()
    
    try:
        await CallbackQuery.answer()
    except:
        pass
        
    mystic = await CallbackQuery.message.reply_text(
        "🔄 در حال پردازش پخش تلویزیون..."
    )
    
    try:
        # بررسی اینکه آیا کانال در لیست موجود است
        if channel_id not in TV_CHANNELS:
            return await mystic.edit_text("❌ کانال تلویزیونی یافت نشد!")
            
        stream_url = TV_CHANNELS[channel_id]
        
        # ساخت دیکشنری اطلاعات برای پخش
        details = {
            "title": f"📺 کانال {channel_id.upper()}",
            "link": stream_url,
            "vidid": stream_url,
            "duration_min": 0,  # برای استریم زنده
            "stream_type": "live",
            "channel": True,
        }
        
        ffplay = True if fplay == "f" else None
        
        await stream(
            _,
            mystic,
            user_id,
            details,
            chat_id,
            user_name,
            CallbackQuery.message.chat.id,
            video,
            streamtype="live",
            forceplay=ffplay,
        )
        
    except Exception as e:
        ex_type = type(e).__name__
        err = e if ex_type == "AssistantErr" else f"خطا در پخش: {ex_type}"
        return await mystic.edit_text(err)
        
    await mystic.delete()

# دستور برای نمایش لیست کانال‌های موجود
@app.on_message(filters.command("tv"))
async def tv_command(client, message):
    buttons = []
    for channel_id in TV_CHANNELS:
        buttons.append([
            InlineKeyboardButton(
                text=f"📺 {channel_id.upper()}",
                callback_data=f"TVStream_{channel_id}|{message.from_user.id}|v|c|f"
            )
        ])
    
    await message.reply_text(
        "**📺 لیست کانال‌های تلویزیونی موجود:**\n\n"
        "برای پخش روی کانال مورد نظر کلیک کنید.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
