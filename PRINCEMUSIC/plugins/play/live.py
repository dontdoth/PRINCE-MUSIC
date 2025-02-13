from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from PRINCEMUSIC import YouTube, app
from PRINCEMUSIC.utils.channelplay import get_channeplayCB
from PRINCEMUSIC.utils.decorators.language import languageCB
from PRINCEMUSIC.utils.stream.stream import stream
from config import BANNED_USERS

# دیکشنری‌های محتوا
TV_CHANNELS = {
    "pmc": "https://hls.pmchd.live/hls/stream.m3u8",
    "manoto": "https://live.manototv.com/live/manoto_tv.m3u8",
    "bbc": "https://bbcpersian-live.bbcfmt.hs.llnwd.net/stream.m3u8",
}

SATELLITE_CHANNELS = {
    "gem_tv": "https://stream.gemtv.live/live/gem_tv.m3u8",
    "gem_series": "https://stream.gemtv.live/live/gem_series.m3u8",
    "gem_river": "https://stream.gemtv.live/live/gem_river.m3u8",
}

RADIO_CHANNELS = {
    "radio_javan": "https://stream.radiojavan.com/radiojavan",
    "radio_farda": "https://stream.radiofarda.com/live",
    "bbc_persian": "https://stream.bbcpersian.com/radio",
}

MOVIES_CHANNELS = {
    "film_net": "https://stream.filmnet.com/live",
    "namava": "https://stream.namava.com/live",
    "filimo": "https://stream.filimo.com/live",
}

@app.on_message(filters.command(["panel", "پنل"]))
async def panel_command(client, message):
    buttons = [
        [
            InlineKeyboardButton("📺 تلویزیون", callback_data="panel_tv"),
            InlineKeyboardButton("🛰 ماهواره", callback_data="panel_satellite")
        ],
        [
            InlineKeyboardButton("📻 رادیو", callback_data="panel_radio"),
            InlineKeyboardButton("🎬 فیلم و سریال", callback_data="panel_movies")
        ],
        [
            InlineKeyboardButton("❌ بستن", callback_data="close_panel")
        ]
    ]
    
    await message.reply_text(
        "**🎯 به پنل پخش زنده خوش آمدید**\n\n"
        "📍 لطفا یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_callback_query(filters.regex("^panel_"))
async def panel_callback(client, callback_query):
    data = callback_query.data.split("_")[1]
    
    if data == "tv":
        buttons = []
        for channel_id, url in TV_CHANNELS.items():
            buttons.append([
                InlineKeyboardButton(
                    f"📺 {channel_id.upper()}", 
                    callback_data=f"stream_tv_{channel_id}|{callback_query.from_user.id}|v|c|f"
                )
            ])
        title = "📺 کانال‌های تلویزیونی"
        
    elif data == "satellite":
        buttons = []
        for channel_id, url in SATELLITE_CHANNELS.items():
            buttons.append([
                InlineKeyboardButton(
                    f"🛰 {channel_id.upper()}", 
                    callback_data=f"stream_sat_{channel_id}|{callback_query.from_user.id}|v|c|f"
                )
            ])
        title = "🛰 کانال‌های ماهواره‌ای"
        
    elif data == "radio":
        buttons = []
        for channel_id, url in RADIO_CHANNELS.items():
            buttons.append([
                InlineKeyboardButton(
                    f"📻 {channel_id.upper()}", 
                    callback_data=f"stream_radio_{channel_id}|{callback_query.from_user.id}|a|c|f"
                )
            ])
        title = "📻 ایستگاه‌های رادیویی"
        
    elif data == "movies":
        buttons = []
        for channel_id, url in MOVIES_CHANNELS.items():
            buttons.append([
                InlineKeyboardButton(
                    f"🎬 {channel_id.upper()}", 
                    callback_data=f"stream_movie_{channel_id}|{callback_query.from_user.id}|v|c|f"
                )
            ])
        title = "🎬 پخش فیلم و سریال"
    
    buttons.append([
        InlineKeyboardButton("🏠 بازگشت به منو", callback_data="panel_main"),
        InlineKeyboardButton("❌ بستن", callback_data="close_panel")
    ])
    
    await callback_query.edit_message_text(
        f"**{title}**\n\n"
        "📍 لطفا یکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_callback_query(filters.regex("^stream_"))
async def stream_callback(client, callback_query):
    data = callback_query.data.split("_")
    stream_type = data[1]  # tv, sat, radio, movie
    channel_id = data[2].split("|")[0]
    user_id = data[2].split("|")[1]
    
    if callback_query.from_user.id != int(user_id):
        return await callback_query.answer("این دکمه برای شما نیست!", show_alert=True)
    
    # انتخاب دیکشنری مناسب براساس نوع استریم
    if stream_type == "tv":
        channels_dict = TV_CHANNELS
        stream_title = "📺 تلویزیون"
    elif stream_type == "sat":
        channels_dict = SATELLITE_CHANNELS
        stream_title = "🛰 ماهواره"
    elif stream_type == "radio":
        channels_dict = RADIO_CHANNELS
        stream_title = "📻 رادیو"
    elif stream_type == "movie":
        channels_dict = MOVIES_CHANNELS
        stream_title = "🎬 فیلم و سریال"
    
    try:
        stream_url = channels_dict[channel_id]
        
        mystic = await callback_query.message.reply_text(
            f"🔄 در حال پردازش پخش {stream_title}..."
        )
        
        details = {
            "title": f"{stream_title} - {channel_id.upper()}",
            "link": stream_url,
            "vidid": stream_url,
            "duration_min": 0,
            "stream_type": "live",
            "channel": True,
        }
        
        # ایجاد یک دیکشنری برای متن‌های مورد نیاز
        language_dict = {
            "play_1": "🎵 پردازش درخواست...",
            "play_2": "🎵 پردازش درخواست در چنل...",
            "play_3": "خطا در پردازش استریم!",
            "general_2": "خطای عمومی: {0}",
            "playcb_1": "این دکمه برای شما نیست!"
        }
        
        await stream(
            language_dict,  # پاس دادن دیکشنری زبان
            mystic,
            user_id,
            details,
            callback_query.message.chat.id,
            callback_query.from_user.first_name,
            callback_query.message.chat.id,
            video=True if stream_type != "radio" else False,
            streamtype="live",
            forceplay=True
        )
        
    except Exception as e:
        await mystic.edit_text(f"❌ خطا در پخش: {str(e)}")
        return
    
    await callback_query.message.delete()
    await mystic.delete()

@app.on_callback_query(filters.regex("panel_main"))
async def return_to_main_panel(client, callback_query):
    buttons = [
        [
            InlineKeyboardButton("📺 تلویزیون", callback_data="panel_tv"),
            InlineKeyboardButton("🛰 ماهواره", callback_data="panel_satellite")
        ],
        [
            InlineKeyboardButton("📻 رادیو", callback_data="panel_radio"),
            InlineKeyboardButton("🎬 فیلم و سریال", callback_data="panel_movies")
        ],
        [
            InlineKeyboardButton("❌ بستن", callback_data="close_panel")
        ]
    ]
    
    await callback_query.edit_message_text(
        "**🎯 به پنل پخش زنده خوش آمدید**\n\n"
        "📍 لطفا یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_callback_query(filters.regex("close_panel"))
async def close_panel(client, callback_query):
    await callback_query.message.delete()
