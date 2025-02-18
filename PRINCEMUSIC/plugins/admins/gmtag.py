from PRINCEMUSIC import app 
import asyncio
import random
from pyrogram import Client, filters
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import UserNotParticipant
from pyrogram.types import ChatPermissions

spam_chats = []

EMOJI = [ "🦋🦋🦋🦋🦋",
          "🧚🌸🧋🍬🫖",
          "🥀🌷🌹🌺💐",
          "🌸🌿💮🌱🌵",
          "❤️💚💙💜🖤",
          "💓💕💞💗💖",
          "🌸💐🌺🌹🦋",
          "🍔🦪🍛🍲🥗",
          "🍎🍓🍒🍑🌶️",
          "🧋🥤🧋🥛🍷",
          "🍬🍭🧁🎂🍡",
          "🍨🧉🍺☕🍻",
          "🥪🥧🍦🍥🍚",
          "🫖☕🍹🍷🥛",
          "☕🧃🍩🍦🍙",
          "🍁🌾💮🍂🌿",
          "🌨️🌥️⛈️🌩️🌧️",
          "🌷🏵️🌸🌺💐",
          "💮🌼🌻🍀🍁",
          "🧟🦸🦹🧙👸",
          "🧅🍠🥕🌽🥦",
          "🐷🐹🐭🐨🐻‍❄️",
          "🦋🐇🐀🐈🐈‍⬛",
          "🌼🌳🌲🌴🌵",
          "🥩🍋🍐🍈🍇",
          "🍴🍽️🔪🍶🥃",
          "🕌🏰🏩⛩️🏩",
          "🎉🎊🎈🎂🎀",
          "🪴🌵🌴🌳🌲",
          "🎄🎋🎍🎑🎎",
          "🦅🦜🕊️🦤🦢",
          "🦤🦩🦚🦃🦆",
          "🐬🦭🦈🐋🐳",
          "🐔🐟🐠🐡🦐",
          "🦩🦀🦑🐙🦪",
          "🐦🦂🕷️🕸️🐚",
          "🥪🍰🥧🍨🍨",
          " 🥬🍉🧁🧇",
        ]

TAGMES = [ " **➠ شب بخیر 🌚** ",
           " **➠ ساکت باش و بخواب 🙊** ",
           " **➠ گوشی رو بذار کنار و بخواب، وگرنه روح میاد 👻** ",
           " **➠ عزیزم روز میتونی بخوابی، الان بگیر بخواب 🥲** ",
           " **➠ مامان ببین داره با دوست دخترش حرف میزنه زیر پتو، نمیخوابه 😜** ",
           " **➠ بابا ببین پسرت تمام شب داره با گوشی ور میره 🤭** ",
           " **➠ عزیزم امشب برنامه بذاریم..؟ 🌠** ",
           " **➠ شب بخیر، خواب‌های خوب، مراقب خودت باش 🙂** ",
           " **➠ شب بخیر، خواب‌های شیرین، مراقب خودت باش ✨** ",
           " **➠ خیلی دیر وقته، بخواب، شب بخیر 🌌** ",
           " **➠ مامان ببین ساعت ۱۱ شده هنوز داره با گوشی ور میره نمیخوابه 🕦** ",
           " **➠ فردا مدرسه نداری که تا الان بیداری؟ 🏫** ",
           " **➠ عزیزم، شب بخیر، خواب خوش 😊** ",
           " **➠ امشب خیلی سرده، راحت و زود میخوابم 🌼** ",
           " **➠ عزیز دلم، شب بخیر 🌷** ",
           " **➠ من میرم بخوابم، شب بخیر و خواب خوش 🏵️** ",
           " **➠ سلام و درود، شب بخیر 🍃** ",
           " **➠ هی عزیزم چطوری؟ نمیخوای بخوابی؟ ☃️** ",
           " **➠ شب بخیر، خیلی دیر وقته ⛄** ",
           " **➠ من میرم گریه کنم، یعنی بخوابم شب بخیر 😁** ",
           " **➠ به ماهی میگن فیش، شب بخیر عزیزم دلتنگم نشو، دارم میرم بخوابم 🌄** ",
           " **➠ شب پر نور بخیر 🤭** ",
           " **➠ شب فرا رسیده، روز تمام شده، ماه جای خورشید رو گرفته 😊** ",
           " **➠ امیدوارم همه آرزوهات برآورده بشه ❤️** ",
           " **➠ شب بخیر و رویاهای شیرین 💚** ",
           " **➠ شب بخیر، خوابم میاد 🥱** ",
           " **➠ دوست عزیز شب بخیر 💤** ",
           " **➠ عزیزم امشب برنامه بذاریم 🥰** ",
           " **➠ این موقع شب بیداری چیکار میکنی، نمیخوای بخوابی؟ 😜** ",
           " **➠ چشمات رو ببند و راحت بخواب، فرشته‌ها امشب مراقبت هستند 💫** "
           ]

VC_TAG = [ "**➠ صبح بخیر، چطوری 🐱**",
         "**➠ صبح بخیر، صبح شده نمیخوای بیدار شی 🌤️**",
         "**➠ صبح بخیر عزیزم، چای بخور ☕**",
         "**➠ زود پاشو، مدرسه نمیخوای بری؟ 🏫**",
         "**➠ صبح بخیر، آروم از تخت بیا پایین وگرنه آب میریزم روت 🧊**",
         "**➠ عزیزم پاشو و زود آماده شو، صبحانه حاضره 🫕**",
         "**➠ امروز نمیخوای بری سر کار؟ هنوز بیدار نشدی 🏣**",
         "**➠ صبح بخیر دوست من، قهوه/چای میل داری؟ ☕🍵**",
         "**➠ عزیزم ساعت ۸ میشه، هنوز بیدار نشدی 🕖**",
         "**➠ ای فرزند خوابالو بیدار شو... ☃️**",
         "**➠ صبح بخیر، روز خوبی داشته باشی... 🌄**",
         "**➠ صبح بخیر، روز خوبی داشته باشی... 🪴**",
         "**➠ صبح بخیر عزیزم، حالت چطوره 😇**",
         "**➠ مامان ببین این تنبل هنوز خوابه... 😵‍💫**",
         "**➠ تمام شب داشتی با گوشی ور میرفتی که الان نمیتونی بیدار شی... 😏**",
         "**➠ عزیزم صبح بخیر پاشو و به همه دوستان تو گروه صبح بخیر بگو... 🌟**",
         "**➠ بابا این هنوز بیدار نشده، وقت مدرسه داره تموم میشه... 🥲**",
         "**➠ عزیزم صبح بخیر، چیکار میکنی... 😅**",
         "**➠ صبح بخیر رفیق، صبحانه خوردی... 🍳**"
        ]

@app.on_message(filters.command(["gntag", "tagmember" ], prefixes=["/", "@", "#"]))
async def mentionall(client, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("๏ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ғᴏʀ ɢʀᴏᴜᴘs.")

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
        return await message.reply("๏ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ʙᴀʙʏ, ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴛᴀɢ ᴍᴇᴍʙᴇʀs. ")

    if message.reply_to_message and message.text:
        return await message.reply("/tagall ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ ᴛʏᴘᴇ ʟɪᴋᴇ ᴛʜɪs / ʀᴇᴘʟʏ ᴀɴʏ ᴍᴇssᴀɢᴇ ɴᴇxᴛ ᴛɪᴍᴇ ʙᴏᴛ ᴛᴀɢɢɪɴɢ...")
    elif message.text:
        mode = "text_on_cmd"
        msg = message.text
    elif message.reply_to_message:
        mode = "text_on_reply"
        msg = message.reply_to_message
        if not msg:
            return await message.reply("/tagall ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ ᴛʏᴘᴇ ʟɪᴋᴇ ᴛʜɪs / ʀᴇᴘʟʏ ᴀɴʏ ᴍᴇssᴀɢᴇ ɴᴇxᴛ ᴛɪᴍᴇ ғᴏᴛ ᴛᴀɢɢɪɴɢ...")
    else:
        return await message.reply("/tagall ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ ᴛʏᴘᴇ ʟɪᴋᴇ ᴛʜɪs / ʀᴇᴘʟʏ ᴀɴʏ ᴍᴇssᴀɢᴇ ɴᴇxᴛ ᴛɪᴍᴇ ʙᴏᴛ ᴛᴀɢɢɪɴɢ...")
    if chat_id in spam_chats:
        return await message.reply("๏ ᴘʟᴇᴀsᴇ ᴀᴛ ғɪʀsᴛ sᴛᴏᴘ ʀᴜɴɴɪɴɢ ᴍᴇɴᴛɪᴏɴ ᴘʀᴏᴄᴇss...")
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


@app.on_message(filters.command(["gmtag"], prefixes=["/", "@", "#"]))
async def mention_allvc(client, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("๏ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ғᴏʀ ɢʀᴏᴜᴘs.")

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
        return await message.reply("๏ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ʙᴀʙʏ, ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴛᴀɢ ᴍᴇᴍʙᴇʀs. ")
    if chat_id in spam_chats:
        return await message.reply("๏ ᴘʟᴇᴀsᴇ ᴀᴛ ғɪʀsᴛ sᴛᴏᴘ ʀᴜɴɴɪɴɢ ᴍᴇɴᴛɪᴏɴ ᴘʀᴏᴄᴇss...")
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
            txt = f"{usrtxt} {random.choice(VC_TAG)}"
            await client.send_message(chat_id, txt)
            await asyncio.sleep(4)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass



@app.on_message(filters.command(["gmstop", "gnstop", "cancle"]))
async def cancel_spam(client, message):
    if not message.chat.id in spam_chats:
        return await message.reply("๏ ᴄᴜʀʀᴇɴᴛʟʏ ɪ'ᴍ ɴᴏᴛ ᴛᴀɢɢɪɴɢ ʙᴀʙʏ.")
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
        return await message.reply("๏ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ʙᴀʙʏ, ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴛᴀɢ ᴍᴇᴍʙᴇʀs.")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.reply("๏ ᴍᴇɴᴛɪᴏɴ ᴘʀᴏᴄᴇss sᴛᴏᴘᴘᴇᴅ ๏")


