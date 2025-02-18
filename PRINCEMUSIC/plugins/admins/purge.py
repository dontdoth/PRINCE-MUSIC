from asyncio import sleep
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.errors import MessageDeleteForbidden, RPCError
from pyrogram.types import Message
from PRINCEMUSIC.utils.Shukla_ban import admin_filter
from PRINCEMUSIC import app

@app.on_message(filters.command(["پاکسازی", "حذف پیام"]) & admin_filter)
async def purge(app: app, msg: Message):
    
    if msg.chat.type != ChatType.SUPERGROUP:
        await msg.reply_text(text="**❌ این دستور فقط در سوپرگروه قابل اجراست**") 
        return

    if msg.reply_to_message:
        message_ids = list(range(msg.reply_to_message.id, msg.id))

        def divide_chunks(l: list, n: int = 100000): # افزایش محدودیت به 100 هزار
            for i in range(0, len(l), n):
                yield l[i : i + n]

        m_list = list(divide_chunks(message_ids))

        try:
            for plist in m_list:
                await app.delete_messages(
                    chat_id=msg.chat.id,
                    message_ids=plist,
                    revoke=True
                )
            await msg.delete()
            
        except MessageDeleteForbidden:
            await msg.reply_text(text="**❌ خطا در حذف پیام‌ها! ممکن است پیام‌ها قدیمی باشند یا دسترسی کافی نداشته باشم**")
            return
            
        except RPCError as ef:
            await msg.reply_text(text=f"**⚠️ خطایی رخ داد:\n<code>{ef}</code>**")
            
        count_del_msg = len(message_ids)
        sumit = await msg.reply_text(text=f"✅ تعداد {count_del_msg} پیام با موفقیت حذف شد")
        await sleep(3)
        await sumit.delete()
        return
        
    await msg.reply_text("**⚠️ لطفا روی پیام مورد نظر ریپلای کنید**")
    return

@app.on_message(filters.command(["پاکسازی سریع", "حذف سریع"]) & admin_filter) 
async def spurge(app: app, msg: Message):

    if msg.chat.type != ChatType.SUPERGROUP:
        await msg.reply_text(text="**❌ این دستور فقط در سوپرگروه قابل اجراست**")
        return

    if msg.reply_to_message:
        message_ids = list(range(msg.reply_to_message.id, msg.id))

        def divide_chunks(l: list, n: int = 100000):
            for i in range(0, len(l), n):
                yield l[i : i + n]

        m_list = list(divide_chunks(message_ids))

        try:
            for plist in m_list:
                # حذف انواع مختلف پیام
                await app.delete_messages(
                    chat_id=msg.chat.id,
                    message_ids=plist,
                    revoke=True
                )
            await msg.delete()
            
        except MessageDeleteForbidden:
            await msg.reply_text(text="**❌ خطا در حذف پیام‌ها! ممکن است پیام‌ها قدیمی باشند یا دسترسی کافی نداشته باشم**")
            return
            
        except RPCError as ef:
            await msg.reply_text(text=f"**⚠️ خطایی رخ داد:\n<code>{ef}</code>**")
            return
            
    await msg.reply_text("**⚠️ لطفا روی پیام مورد نظر ریپلای کنید**") 
    return

@app.on_message(filters.command(["حذف", "پاک کردن"]) & admin_filter)
async def del_msg(app: app, msg: Message):
    if msg.chat.type != ChatType.SUPERGROUP:
        await msg.reply_text(text="**❌ این دستور فقط در سوپرگروه قابل اجراست**")
        return
        
    if msg.reply_to_message:
        # حذف سریع انواع پیام‌ها
        await msg.delete()
        await app.delete_messages(
            chat_id=msg.chat.id,
            message_ids=msg.reply_to_message.id
        )
    else:
        await msg.reply_text(text="**⚠️ لطفا روی پیام مورد نظر برای حذف ریپلای کنید**")
        return

# اضافه کردن فیلتر برای پاکسازی انواع خاص پیام
@app.on_message(filters.command(["پاکسازی رسانه", "حذف رسانه"]) & admin_filter)
async def purge_media(app: app, msg: Message):
    if msg.chat.type != ChatType.SUPERGROUP:
        await msg.reply_text(text="**❌ این دستور فقط در سوپرگروه قابل اجراست**")
        return

    if msg.reply_to_message:
        message_ids = []
        for message_id in range(msg.reply_to_message.id, msg.id):
            message = await app.get_messages(msg.chat.id, message_id)
            if message.media:
                message_ids.append(message_id)

        if not message_ids:
            await msg.reply_text("**⚠️ هیچ رسانه‌ای برای حذف یافت نشد**")
            return

        try:
            await app.delete_messages(
                chat_id=msg.chat.id,
                message_ids=message_ids,
                revoke=True
            )
            await msg.delete()
            
            count = len(message_ids)
            sumit = await msg.reply_text(f"✅ تعداد {count} رسانه با موفقیت حذف شد")
            await sleep(3)
            await sumit.delete()
            
        except RPCError as ef:
            await msg.reply_text(f"**⚠️ خطایی رخ داد:\n<code>{ef}</code>**")
            
    else:
        await msg.reply_text("**⚠️ لطفا روی پیام مورد نظر ریپلای کنید**")
