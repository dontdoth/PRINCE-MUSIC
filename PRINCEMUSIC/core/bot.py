from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode
import config
from ..logging import LOGGER

class PRINCE(Client):
    def __init__(self):
        LOGGER(__name__).info(f"Starting Bot...")
        super().__init__(
            name="PRINCEMUSIC",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()
        try:
            self.id = self.me.id
            self.name = self.me.first_name + " " + (self.me.last_name or "")
            self.username = self.me.username
            self.mention = self.me.mention
            
            # اول چک کنیم که LOGGER_ID تنظیم شده است
            if not config.LOGGER_ID:
                LOGGER(__name__).error("LOGGER_ID is not set in config!")
                exit()

            # سعی می‌کنیم اطلاعات گروه لاگ را دریافت کنیم
            try:
                log_group = await self.get_chat(config.LOGGER_ID)
                LOGGER(__name__).info(f"Successfully connected to log group: {log_group.title}")
            except Exception as e:
                LOGGER(__name__).error(f"Failed to get log group info: {str(e)}")
                exit()

            # چک کردن دسترسی‌های ربات در گروه لاگ
            try:
                bot_member = await self.get_chat_member(config.LOGGER_ID, self.id)
                if bot_member.status != ChatMemberStatus.ADMINISTRATOR:
                    LOGGER(__name__).error("Bot needs to be admin in log group!")
                    exit()
            except Exception as e:
                LOGGER(__name__).error(f"Failed to check bot permissions: {str(e)}")
                exit()

            # ارسال پیام شروع
            try:
                await self.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"<u><b>» {self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b></u>\n\nɪᴅ : <code>{self.id}</code>\nɴᴀᴍᴇ : {self.name}\nᴜsᴇʀɴᴀᴍᴇ : @{self.username}",
                )
                LOGGER(__name__).info(f"Music Bot Started as {self.name}")
            except Exception as e:
                LOGGER(__name__).error(f"Failed to send start message: {str(e)}")
                exit()

        except Exception as e:
            LOGGER(__name__).error(f"Critical error during bot startup: {str(e)}")
            exit()

    async def stop(self):
        await super().stop()
