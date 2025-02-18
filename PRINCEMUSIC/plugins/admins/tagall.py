from PRINCEMUSIC import app 
import asyncio
import random
from pyrogram import Client, filters
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import UserNotParticipant
from pyrogram.types import ChatPermissions

spam_chats = []

EMOJI = [
    "🦋🦋🦋🦋🦋",
    "🧚‍♀️🌸🧋🍬🫖",
    "🥀🌷🌹🌺💐",
    "🌸🌿💮🌱🌵",
    "❤️💚💙💜🖤",
    "💓💕💞💗💖",
    "🌸💐🌺🌹🦋",
    "🍔🦪🍛🍲🥗",
    "🍎🍓🍒🍑🌶️",
    "🧋🥤🧃🥛🍷",
    "🍬🍭🧁🎂🍡",
    "🍨🧉🍺☕🍻",
    "🥪🥧🍦🍥🍚",
    "🫖☕🍹🍷🥛",
    "☕🧃🍩🍦🍙",
    "🍁🌾💮🍂🌿",
    "🌨️🌥️⛈️🌩️🌧️",
    "🌷🏵️🌸🌺💐",
    "💮🌼🌻🍀🍁",
    "🎭👻👾🎪🎨",
    "🌺🌸🌼🌻🌹",
    "🎪🎭🎨🎪🎫",
    "🍓🍎🍉🍊🍋",
    "🍌🍍🍐🍇🥝",
    "🥐🥨🥖🥯🥞",
    "🧇🧀🥗🥙🥪",
    "🌭🍔🍟🍕🥩",
    "🍗🍖🦴🌮🌯",
    "🥘🍝🥫🫕🥣",
    "🍲🍛🍜🍢🍱",
    "🍚🍤🍣🦪🍘",
    "🍡🍧🍨🍦🥧",
    "🧁🍰🎂🍮🍭",
    "🍬🍫🍿🍩🍪",
    "🌰🥜🍯🧂🧈",
    "🍷🥂🍻🍺🍶",
    "🧃🧊🥤🧋🍹",
    "🍾🥛☕🫖🍵",
    "🎵🎶🎼🎹🎸",
    "🎺🎻🥁🎤🎧"
]

TAGMES = [
    "**سلام عزیزم کجایی؟ 🤗**",
    "**دلم برات تنگ شده 💝**",
    "**بیا آنلاین شو دیگه 😊**",
    "**چرا جواب نمیدی؟ 🥺**",
    "**کجا رفتی یهو؟ 👀**",
    "**بیا پیوی کارت دارم 😉**",
    "**چه خبر؟ 😃**",
    "**خوبی عزیزم؟ ❤️**",
    "**امروز چیکارا کردی؟ 🌸**",
    "**میای بریم بیرون؟ 🎈**",
    "**حوصلم سر رفته 🥱**",
    "**پایه ای بریم گردش؟ 🌟**",
    "**چرا اینقدر خوشگلی تو؟ 😍**",
    "**دوستت دارم 💕**",
    "**بیا باهم حرف بزنیم 🗣️**",
    "**چرا اینقدر ماهی؟ 🌙**",
    "**کی میای پیشم؟ 🏃‍♀️**",
    "**دلم هواتو کرده 💫**",
    "**یه پیام بده خب 📝**",
    "**کجایی پس؟ 👣**",
    "**بیا وویس چت 🎤**",
    "**چرا آفلاینی؟ 💭**",
    "**پیام هامو نمیبینی؟ 👀**",
    "**یه زنگ بزن 📞**",
    "**قهری باهام؟ 🥺**",
    "**میشه برگردی؟ 🙏**",
    "**خیلی دوست دارم ❤️**",
    "**بیا یه فیلم ببینیم 🎬**",
    "**موزیک گوش میدی؟ 🎵**",
    "**امشب بیداری؟ 🌙**",
    "**صبحت بخیر عزیزم 🌅**",
    "**شب بخیر گلم 🌃**",
    "**خوابیدی هنوز؟ 😴**",
    "**پاشو دیگه ⏰**",
    "**ناهار خوردی؟ 🍜**",
    "**چی پختی امروز؟ 👩‍🍳**",
    "**میای بریم خرید؟ 🛍️**",
    "**هوا چطوره اونجا? ⛅**",
    "**بارون میاد? 🌧️**",
    "**چه خبر از درس و کار? 📚**",
    "**خسته نباشی عزیزم 💪**",
    "**یه عکس بفرست 📸**",
    "**کی میای آنلاین? 🟢**",
    "**دلم برات یه ذره شده 💗**",
    "**یادم کردی امروز? 🤔**",
    "**بیا چت کنیم 💭**",
    "**چرا جواب نمیدی خب? 📱**",
    "**کجای شهری? 🌆**",
    "**بیرون بارونه? ⛈️**",
    "**چیکار میکنی? 👀**",
    "**حالت چطوره? 💝**",
    "**خوش میگذره? 🎉**",
    "**منو فراموش کردی? 💔**",
    "**یادته قدیما رو? 🎭**",
    "**بیا یه بازی کنیم 🎮**",
    "**حوصلت سر نرفته? 🥱**",
    "**چه خبر از دوستات? 👥**",
    "**مهمونی نمیای? 🎊**",
    "**کی برمیگردی? 🔄**",
    "**دوستت دارم خیلی 💘**",
    "**بیا پیش من 🏃**",
    "**کجا غیبت زد یهو? 👻**",
    "**دلتنگتم خیلی 💖**",
    "**یه پیام کوچولو بده 📨**",
    "**چرا دیر جواب میدی? ⏳**",
    "**یادی از ما نمیکنی 🥺**",
    "**خیلی بی معرفتی 😔**",
    "**بیا یکم حرف بزنیم 🗣️**",
    "**چقدر دلم برات تنگه 💗**",
    "**کاش پیشم بودی 🌟**",
    "**یه زنگ بزن صداتو بشنوم 📞**",
    "**امروز چه خبر? 📰**",
    "**نبینم غمتو 🥺**",
    "**لبخند یادت نره 😊**",
    "**مواظب خودت باش ❤️**",
    "**دوست دارم عزیزم 💕**",
    "**قربونت برم من 🥰**",
    "**فدات شم الهی 💖**",
    "**بوس به روی ماهت 😘**",
    "**عشق منی تو 💝**",
    "**زندگیمی عزیزم ❤️**",
    "**نفسمی گلم 💗**",
    "**عشق دلمی 💓**",
    "**ماه منی تو 🌙**",
    "**خوشگل خانوم کجایی؟ 👸**",
    "**آقای گل کجایی؟ 🤴**"
]

@app.on_message(filters.command(["تگ", "اسپم", "تگ_همه", "تگ_کاربران"], prefixes=["/", "@", "#"]))
async def mentionall(client, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("این دستور فقط در گروه‌ها کار می‌کند.")

    is_admin = False
    try:
        participant = await client.get_chat_member(chat_id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("شما ادمین نیستید، فقط ادمین‌ها می‌توانند از این دستور استفاده کنند.")

    if message.reply_to_message and message.text:
        return await message.reply("لطفا به این شکل تگ کنید: /تگ یا روی پیام ریپلای کنید")
    elif message.text:
        mode = "text_on_cmd"
        msg = message.text
    elif message.reply_to_message:
        mode = "text_on_reply"
        msg = message.reply_to_message
        if not msg:
            return await message.reply("لطفا به این شکل تگ کنید: /تگ یا روی پیام ریپلای کنید")
    else:
        return await message.reply("لطفا به این شکل تگ کنید: /تگ یا روی پیام ریپلای کنید")

    if chat_id in spam_chats:
        return await message.reply("لطفا صبر کنید تا فرایند قبلی تمام شود...")
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        if usr.user.is_bot:
            continue
        usrnum += 1
        usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id}) "

        if usrnum == 1:
            if mode == "text_on_cmd":
                txt = f"{usrtxt} {random.choice(TAGMES)}"
                await client.send_message(chat_id, txt)
            elif mode == "text_on_reply":
                await msg.reply(f"[{random.choice(EMOJI)}](tg://user?id={usr.user.id})")
            await asyncio.sleep(4)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass

@app.on_message(filters.command(["توقف_تگ", "پایان_تگ"]))
async def cancel_spam(client, message):
    if not message.chat.id in spam_chats:
        return await message.reply("در حال حاضر هیچ تگی در حال اجرا نیست...")
    is_admin = False
    try:
        participant = await client.get_chat_member(message.chat.id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("شما ادمین نیستید، فقط ادمین‌ها می‌توانند تگ را متوقف کنند.")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.reply("♦ تگ متوقف شد ♦")
