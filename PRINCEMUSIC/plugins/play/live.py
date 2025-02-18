from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from PRINCEMUSIC import YouTube, app
from PRINCEMUSIC.utils.channelplay import get_channeplayCB
from PRINCEMUSIC.utils.decorators.language import languageCB
from PRINCEMUSIC.utils.stream.stream import stream
from config import BANNED_USERS

# دیکشنری‌های محتوا
TV_CHANNELS = {
    "bbc_persian": "http://eja.tv/?6360d8abbeaad1d477b020840e3eb81d9b76fbd495ca8b4196dcf3f13753266c",
    "pmc": "http://eja.tv/?439cd65f2c94b2b51df36c48f0dc919aebc217eeb1b730db96e73de977064092",
    "fars": "http://eja.tv/?8f12561a7500b6671fdea74df8baa514cfec21729ab6876d151509fd5d77be6d",
    "khalijefars": "http://eja.tv/?17f037a1d6ab4dd58ee001d443e2f44ef8c186e96b9d422951a80516a461a4aa",
    "bravo_farsi": "http://eja.tv/?e61c2c93618ffbf3660aa1126f5ffb27c14a61a6680d15b91e13a04697be48e2",
    "hadi_tv": "http://eja.tv/?17f037a1d6ab4dd58ee001d443e2f44ef8c186e96b9d422951a80516a461a4aa"
}

MUSIC_CHANNELS = {
    "music_box": "http://eja.tv/?e9660a4a17b197db62830e82774b557ddfd79ac46b57646a1658b98fd737b042",
    "1hd_music": "http://eja.tv/?84972ee8c5dc50f80d90108c944f8e0c60b434ed0f985febcc4c83e1bd5d6078",
    "albkanale": "http://eja.tv/?a778ad73d76433f315cff2a8caa3802a0eb6b35a90a882f4a22ba99979686792",
    "30a_music": "http://eja.tv/?6ca525e59df530dd493d3c259da068a4f643683198d58ecddd398d4c59292e40",
    "a2i_music": "http://eja.tv/?edf426412ff83c4860f6bc133c681812a010e1b2cb581edb474c043b688a57cd",
    "avang": "http://eja.tv/?2bead70fc6047d6ca249655db1846a43e53be81f9d5a999606122d2a1ae7c703",
    "persiana_music": "http://eja.tv/?08ae6d6a4ff512d93d8c32de0eebc0f4993443763ec42e02c38fe0547ea73648",
    "navahang": "http://eja.tv/?10d123861cd18d81099e6611ab936a3d62ab262f7a2a2daf63c85b508b88dd26",
    "tatlises": "http://eja.tv/?8b1fda135d6d300c82de6685e1a297d6953aba0b387997400f82b80b3be6eac4",
    "power_turk": "http://eja.tv/?8f12561a7500b6671fdea74df8baa514cfec21729ab6876d151509fd5d77be6d"
}

MOVIES_CHANNELS = {
    "cinema_plus": "http://eja.tv/?18517b421f02614b9a03b61bc03b401bdf6b02acb38f8a1296932a2255ed2bd3",
    "classic_cinema": "http://eja.tv/?cd09669a855f52cb6bdc648cc02a5a18f6cd2471656d8bd0ba2d9be7f863567e",
    "black_cinema": "http://eja.tv/?d430c73877ba5eb0d472dde071281db74d1ffc8d72f111a02c256d476f9077d9",
    "filmrise": "http://eja.tv/?f3e56bc7dad120d7c23467806c2a362f1d7172a86210dcc0820aea97b3813f7a",
    "film_hub": "http://eja.tv/?2bc72dff7e9d05f2f263f797cb8dbf6ce9b081133d9525ec115f6a8db0d446b9",
    "discover_film": "http://eja.tv/?d50bdb7b9e3955308c010d0ad750e97aace4c73245a1c728d29d90378d922bcf",
    "master_video": "http://eja.tv/?2d4917f66b5c93a6f68f0867f025a9dec0c66d2421817d5cc073e36ea005f9ab"
}

GEM_CHANNELS = {
    "gem_academy": "http://eja.tv/?1767e35ad663ffcb582bf7288e2262367dc36d5d76ea2f3ca9eb1542e3b0946c",
    "gem_classic": "http://eja.tv/?ff27dc9eca3ef3bc1310075570f730fa597515aba00ee325c4433ba925610aae",
    "gem_drama": "http://eja.tv/?683a7b9b98f153e0a346d081b666944a5d582088743d4b1082c44f974363d78e",
    "gem_film": "http://eja.tv/?3f3cdb613344d6415f39576d873db5a3d1315f37553da8ed89941679d2435e69",
    "gem_fit": "http://eja.tv/?2bc72dff7e9d05f2f263f797cb8dbf6ce9b081133d9525ec115f6a8db0d446b9"
}

def get_main_panel():
    buttons = [
        [
            InlineKeyboardButton("📺 تلویزیون", callback_data="panel_tv"),
            InlineKeyboardButton("🎵 موزیک", callback_data="panel_music")
        ],
        [
            InlineKeyboardButton("🎬 فیلم و سریال", callback_data="panel_movies"),
            InlineKeyboardButton("💎 شبکه‌های جم", callback_data="panel_gem")
        ],
        [
            InlineKeyboardButton("❌ بستن", callback_data="close_panel")
        ]
    ]
    return InlineKeyboardMarkup(buttons)

@app.on_message(filters.command(["panel", "پنل"]))
async def panel_command(client, message):
    await message.reply_text(
        "**🎯 به پنل پخش زنده خوش آمدید**\n\n"
        "📍 لطفا یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=get_main_panel()
    )

@app.on_callback_query(filters.regex("^panel_"))
async def panel_callback(client, callback_query):
    data = callback_query.data.split("_")[1]
    
    if data == "main":
        await callback_query.edit_message_text(
            "**🎯 به پنل پخش زنده خوش آمدید**\n\n"
            "📍 لطفا یکی از گزینه‌های زیر را انتخاب کنید:",
            reply_markup=get_main_panel()
        )
        return
    
    if data == "tv":
        channels_dict = TV_CHANNELS
        title = "📺 کانال‌های تلویزیونی"
    elif data == "music":
        channels_dict = MUSIC_CHANNELS
        title = "🎵 کانال‌های موسیقی"
    elif data == "movies":
        channels_dict = MOVIES_CHANNELS
        title = "🎬 کانال‌های فیلم و سریال"
    elif data == "gem":
        channels_dict = GEM_CHANNELS
        title = "💎 شبکه‌های جم"
    
    buttons = []
    for channel_id, url in channels_dict.items():
        buttons.append([
            InlineKeyboardButton(
                f"▶️ {channel_id.upper().replace('_', ' ')}", 
                callback_data=f"stream_{data}_{channel_id}|{callback_query.from_user.id}|v|c|f"
            )
        ])
    
    buttons.append([
        InlineKeyboardButton("🏠 بازگشت به منو", callback_data="panel_main"),
        InlineKeyboardButton("❌ بستن", callback_data="close_panel")
    ])
    
    await callback_query.edit_message_text(
        f"**{title}**\n\n"
        "📍 لطفا یکی از کانال‌ها را انتخاب کنید:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_callback_query(filters.regex("^stream_"))
async def stream_callback(client, callback_query):
    try:
        data = callback_query.data.split("_")
        stream_type = data[1]
        channel_id = data[2].split("|")[0]
        user_id = data[2].split("|")[1]
        
        if callback_query.from_user.id != int(user_id):
            return await callback_query.answer("این دکمه برای شما نیست!", show_alert=True)
            
        channels_dict = {
            "tv": TV_CHANNELS,
            "music": MUSIC_CHANNELS,
            "movies": MOVIES_CHANNELS,
            "gem": GEM_CHANNELS
        }[stream_type]
        
        stream_url = channels_dict[channel_id]
        chat_id = callback_query.message.chat.id
        
        mystic = await callback_query.message.reply_text(
            f"🔄 در حال پردازش پخش..."
        )
        
        details = {
            "title": f"{channel_id.upper().replace('_', ' ')}",
            "link": stream_url,
            "vidid": stream_url,
            "duration_min": 0,
            "stream_type": "live",
            "channel": True,
            "thumb": None
        }

        language_dict = {
            "play_1": "🎵 پردازش درخواست...",
            "play_2": "🎵 پردازش درخواست در چنل...",
            "play_3": "خطا در پردازش استریم!",
            "general_2": "خطای عمومی: {0}",
            "playcb_1": "این دکمه برای شما نیست!",
            "str_1": "در حال پردازش...",
            "str_2": "در حال استریم...",
            "str_3": "استریم آغاز شد",
            "stream_1": "استریم یافت شد",
            "stream_2": "پردازش استریم",
            "stream_3": "استریم آماده پخش",
            "stream_4": "پخش زنده آغاز شد",
            "admin_1": "شما ادمین نیستید",
            "admin_2": "فقط ادمین‌ها",
            "admin_3": "مدیریت پخش",
            "processing": "لطفا صبر کنید...",
            "searching": "در حال جستجو...",
            "streaming": "در حال پخش...",
            "playing": "در حال اجرا...",
            "track_1": "عنوان: {0}",
            "track_2": "مدت: {0}",
            "track_3": "درخواست: {0}",
            "queue_1": "در صف پخش",
            "queue_2": "بعدی در صف",
            "queue_3": "اضافه به صف",
            "queue_4": "صف خالی است"
        }
        
        await stream(
            language_dict,
            mystic,
            user_id,
            details,
            chat_id,
            user_name=callback_query.from_user.first_name,
            original_chat_id=chat_id,
            video=True if stream_type != "music" else False,
            streamtype="live",
            forceplay=True
        )
        
    except Exception as e:
        await mystic.edit_text(f"❌ خطا در پخش: {str(e)}")
        return
    
    await callback_query.message.delete()
    await mystic.delete()
    
    await callback_query.message.delete()
    await mystic.delete()
@app.on_callback_query(filters.regex("close_panel"))
async def close_panel(client, callback_query):
    await callback_query.message.delete()
