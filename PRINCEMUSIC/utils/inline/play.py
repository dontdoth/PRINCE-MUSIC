import math
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from PRINCEMUSIC import app
import config
from PRINCEMUSIC.utils.formatters import time_to_seconds
from typing import Union


def track_markup(_, videoid, user_id, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
            )
        ],
    ]
    return buttons


def stream_markup_timer(_, chat_id, played, dur):
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    percentage = (played_sec / duration_sec) * 100
    umm = math.floor(percentage)
    
    if 0 < umm <= 10:
        bar = "◉—————————"
    elif 10 < umm < 20:
        bar = "—◉————————"
    elif 20 <= umm < 30:
        bar = "——◉———————"
    elif 30 <= umm < 40:
        bar = "———◉——————"
    elif 40 <= umm < 50:
        bar = "————◉—————"
    elif 50 <= umm < 60:
        bar = "—————◉————"
    elif 60 <= umm < 70:
        bar = "——————◉———"
    elif 70 <= umm < 80:
        bar = "———————◉——"
    elif 80 <= umm < 95:
        bar = "————————◉—"
    else:
        bar = "—————————◉"

    buttons = [
        [
            InlineKeyboardButton("⏮ 30", callback_data=f"ADMIN Seek|-30|{chat_id}"),
            InlineKeyboardButton("⏭ 30", callback_data=f"ADMIN Seek|+30|{chat_id}"),
        ],
        [
            InlineKeyboardButton("🔇 بی‌صدا", callback_data=f"ADMIN Mute|{chat_id}"),
            InlineKeyboardButton("🔊 باصدا", callback_data=f"ADMIN Unmute|{chat_id}"),
        ],
        [
            InlineKeyboardButton("🎚 تنظیم صدا", callback_data=f"VOL {chat_id}"),
        ],
        [
            InlineKeyboardButton("📋 پلی‌لیست", callback_data="get_top_playlists"),
            InlineKeyboardButton("📊 آمار ویس", callback_data="vcinfo"),
        ],
        [
            InlineKeyboardButton("𝙍𝘼𝙉𝙂𝙀𝙍 ™", callback_data="logo"),
        ],
        [
            InlineKeyboardButton(
                text=f"{played} {bar} {dur}",
                callback_data="GetTimer",
            )
        ],
        [
            InlineKeyboardButton(text="▷", callback_data=f"ADMIN Resume|{chat_id}"),
            InlineKeyboardButton(text="II", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton(text="‣‣I", callback_data=f"ADMIN Skip|{chat_id}"),
            InlineKeyboardButton(text="▢", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        [InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")],
    ]
    return buttons


def stream_markup(_, chat_id):
    buttons = [
        [
            InlineKeyboardButton("⏮ 30", callback_data=f"ADMIN Seek|-30|{chat_id}"),
            InlineKeyboardButton("⏭ 30", callback_data=f"ADMIN Seek|+30|{chat_id}"),
        ],
        [
            InlineKeyboardButton("🔇 بی‌صدا", callback_data=f"ADMIN Mute|{chat_id}"),
            InlineKeyboardButton("🔊 باصدا", callback_data=f"ADMIN Unmute|{chat_id}"),
        ],
        [
            InlineKeyboardButton("🎚 تنظیم صدا", callback_data=f"VOL {chat_id}"),
        ],
        [
            InlineKeyboardButton("📋 پلی‌لیست", callback_data="get_top_playlists"),
            InlineKeyboardButton("📊 آمار ویس", callback_data="vcinfo"),
        ],
        [
            InlineKeyboardButton("𝙍𝘼𝙉𝙂𝙀𝙍 ™", callback_data="logo"),
        ],
        [
            InlineKeyboardButton(text="▷", callback_data=f"ADMIN Resume|{chat_id}"),
            InlineKeyboardButton(text="II", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton(text="‣‣I", callback_data=f"ADMIN Skip|{chat_id}"),
            InlineKeyboardButton(text="▢", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        [InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")],
    ]
    return buttons


def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"SHUKLAPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"SHUKLAPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
        ],
    ]
    return buttons


def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_3"],
                callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
        ],
    ]
    return buttons


def slider_markup(_, videoid, user_id, query, query_type, channel, fplay):
    query = f"{query[:20]}"
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="◁",
                callback_data=f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {query}|{user_id}",
            ),
            InlineKeyboardButton(
                text="▷",
                callback_data=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}",
            ),
        ],
    ]
    return buttons


def volume_markup(_, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="🔈 10%",
                callback_data=f"ADMIN Volume|10|{chat_id}",
            ),
            InlineKeyboardButton(
                text="🔈 25%",
                callback_data=f"ADMIN Volume|25|{chat_id}",
            ),
            InlineKeyboardButton(
                text="🔉 50%",
                callback_data=f"ADMIN Volume|50|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔊 75%",
                callback_data=f"ADMIN Volume|75|{chat_id}",
            ),
            InlineKeyboardButton(
                text="🔊 100%",
                callback_data=f"ADMIN Volume|100|{chat_id}",
            ),
            InlineKeyboardButton(
                text="🔊 150%",
                callback_data=f"ADMIN Volume|150|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔈 صدای سفارشی",
                callback_data=f"ADMIN CustomVolume|{chat_id}",
            )
        ],
        [InlineKeyboardButton(text="🔙 برگشت", callback_data=f"MainMenu|{chat_id}")],
    ]
    return buttons
