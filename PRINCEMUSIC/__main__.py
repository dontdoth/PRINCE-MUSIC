import asyncio
import importlib
import gc
import signal
from typing import Optional
from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall
import aiohttp

import config
from PRINCEMUSIC import LOGGER, app, userbot
from PRINCEMUSIC.core.call import PRINCE
from PRINCEMUSIC.misc import sudo
from PRINCEMUSIC.plugins import ALL_MODULES
from PRINCEMUSIC.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

# Global session storage
sessions = {}

async def cleanup_sessions():
    """Cleanup aiohttp sessions"""
    if sessions:
        for session in sessions.values():
            if not session.closed:
                await session.close()
        sessions.clear()

async def signal_handler():
    """Handle shutdown signals properly"""
    await cleanup_sessions()
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    await asyncio.gather(*tasks, return_exceptions=True)
    loop = asyncio.get_running_loop()
    loop.stop()
    loop.close()

async def init():
    try:
        # Setup signal handlers
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, lambda s=sig: asyncio.create_task(signal_handler()))

        # Create global session
        sessions['main'] = aiohttp.ClientSession()

        # Verify string sessions
        if not any([config.STRING1, config.STRING2, config.STRING3, config.STRING4, config.STRING5]):
            LOGGER(__name__).error(
                "𝐒𝐭𝐫𝐢𝐧𝐠 𝐒𝐞𝐬𝐬𝐢𝐨𝐧 𝐍𝐨𝐭 𝐅𝐢𝐥𝐥𝐞𝐝, 𝐏𝐥𝐞𝐚𝐬𝐞 𝐅𝐢𝐥𝐥 𝐀 𝐏𝐲𝐫𝐨𝐠𝐫𝐚𝐦 𝐒𝐞𝐬𝐬𝐢𝐨𝐧"
            )
            return False

        # Initialize components
        await sudo()
        
        try:
            users = await get_gbanned()
            for user_id in users:
                BANNED_USERS.add(user_id)
            users = await get_banned_users()
            for user_id in users:
                BANNED_USERS.add(user_id)
        except Exception as e:
            LOGGER(__name__).error(f"Failed to load banned users: {e}")

        # Start main app
        await app.start()
        
        # Load modules
        for all_module in ALL_MODULES:
            try:
                importlib.import_module("PRINCEMUSIC.plugins" + all_module)
            except Exception as e:
                LOGGER(__name__).error(f"Failed to load module {all_module}: {e}")
                
        LOGGER("PRINCEMUSIC.plugins").info("𝐀𝐥𝐥 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 𝐋𝐨𝐚𝐝𝐞𝐝 𝐁𝐚𝐛𝐲🥳...")

        # Start userbot
        await userbot.start()
        await PRINCE.start()

        try:
            await PRINCE.stream_call(
                "https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4",
                force_low_memory=True
            )
        except NoActiveGroupCall:
            LOGGER("PRINCEMUSIC").error(
                "𝗣𝗹𝗭 𝗦𝗧𝗔𝗥𝗧 𝗬𝗢𝗨𝗥 𝗟𝗢𝗚 𝗚𝗥𝗢𝗨𝗣 𝗩𝗢𝗜𝗖𝗘𝗖𝗛𝗔𝗧\𝗖𝗛𝗔𝗡𝗡𝗘𝗟\n\n𝗣𝗥𝗜𝗡𝗖𝗘 𝗕𝗢𝗧 𝗦𝗧𝗢𝗣........"
            )
            await cleanup_sessions()
            return False
        except Exception as e:
            LOGGER("PRINCEMUSIC").error(f"Stream call error: {e}")

        await PRINCE.decorators()
        LOGGER("PRINCEMUSIC").info(
            "╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎𝗠𝗔𝗗𝗘 𝗕𝗬 𝗠𝗥 𝗣𝗥𝗜𝗡𝗖𝗘\n╚═════ஜ۩۞۩ஜ════╝"
        )

        await idle()
        return True

    except Exception as e:
        LOGGER("PRINCEMUSIC").error(f"Initialization error: {e}")
        await cleanup_sessions()
        return False

async def shutdown():
    """Cleanup and shutdown"""
    try:
        LOGGER("PRINCEMUSIC").info("Shutting down...")
        
        # Cleanup sessions
        await cleanup_sessions()
        
        # Stop components
        if hasattr(app, 'stop'):
            await app.stop()
        if hasattr(userbot, 'stop'):
            await userbot.stop()
        
        # Cancel all tasks
        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        [task.cancel() for task in tasks]
        await asyncio.gather(*tasks, return_exceptions=True)
        
        LOGGER("PRINCEMUSIC").info("𝗦𝗧𝗢𝗣 𝗣𝗥𝗜𝗡𝗖𝗘 𝗠𝗨𝗦𝗜𝗖🎻 𝗕𝗢𝗧..")
        
    except Exception as e:
        LOGGER("PRINCEMUSIC").error(f"Shutdown error: {e}")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(init())
    except KeyboardInterrupt:
        LOGGER("PRINCEMUSIC").info("Bot stopped by user!")
    except Exception as e:
        LOGGER("PRINCEMUSIC").error(f"Fatal error: {e}")
    finally:
        loop.run_until_complete(shutdown())
        loop.close()
        gc.collect()
