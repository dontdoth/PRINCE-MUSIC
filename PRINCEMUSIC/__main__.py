import asyncio
import importlib
import signal
import sys
import time
import gc
from contextlib import suppress
from typing import Optional
import aiohttp
import psutil
from pyrogram import Client, idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from PRINCEMUSIC import LOGGER, userbot
from PRINCEMUSIC.core.call import PRINCE
from PRINCEMUSIC.misc import sudo
from PRINCEMUSIC.plugins import ALL_MODULES
from PRINCEMUSIC.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS
from custom_dispatcher import CustomDispatcher

# Global Variables
LOAD_MODULES = []
TASKS = []
ACTIVE_CALLS = set()
SESSIONS = {}

class CustomClient(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = CustomDispatcher(self, workers=config.WORKER_COUNT)
        self.start_time = time.time()

    async def start(self):
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name
        self.username = self.me.username
        LOGGER("PRINCEMUSIC").info(f"Bot started as {self.name}")

    async def stop(self):
        await self.dispatcher.stop()
        await super().stop()

async def init_aiohttp_session():
    """Initialize global aiohttp session"""
    if 'session' not in SESSIONS:
        SESSIONS['session'] = aiohttp.ClientSession()
    return SESSIONS['session']

async def cleanup_resources():
    """Cleanup all resources"""
    try:
        # Cleanup sessions
        for session in SESSIONS.values():
            if not session.closed:
                await session.close()
        SESSIONS.clear()

        # Cleanup active calls
        for call in ACTIVE_CALLS:
            try:
                await call.stop()
            except:
                pass
        ACTIVE_CALLS.clear()

        # Cancel all tasks
        for task in TASKS:
            task.cancel()
            with suppress(asyncio.CancelledError):
                await task
        TASKS.clear()

        # Force garbage collection
        gc.collect()

    except Exception as e:
        LOGGER("PRINCEMUSIC").error(f"Error in cleanup: {e}")

async def load_modules():
    """Load all modules"""
    try:
        for module in ALL_MODULES:
            if module not in LOAD_MODULES:
                try:
                    imported_module = importlib.import_module(f"PRINCEMUSIC.plugins.{module}")
                    if hasattr(imported_module, "__mod_name__"):
                        LOAD_MODULES.append(imported_module)
                        LOGGER("Modules").info(f"Successfully loaded: {module}")
                except Exception as e:
                    LOGGER("Modules").error(f"Failed to load {module}: {e}")
    except Exception as e:
        LOGGER("Modules").error(f"Module loading error: {e}")

async def monitor_resources():
    """Monitor system resources"""
    while True:
        try:
            process = psutil.Process()
            memory_usage = process.memory_info().rss / 1024 / 1024  # MB
            
            if memory_usage > config.MEMORY_LIMIT:
                LOGGER("System").warning(f"High memory usage: {memory_usage:.2f}MB")
                gc.collect()
            
            await asyncio.sleep(60)
        except Exception as e:
            LOGGER("System").error(f"Monitoring error: {e}")
            await asyncio.sleep(60)

async def shutdown(signal, loop):
    """Handle shutdown gracefully"""
    LOGGER("PRINCEMUSIC").info(f"Received exit signal {signal.name}")
    
    try:
        # Stop all services
        if hasattr(app, 'stop'):
            await app.stop()
        if hasattr(userbot, 'stop'):
            await userbot.stop()
        
        # Cleanup resources
        await cleanup_resources()
        
        # Stop the event loop
        loop.stop()
        
    except Exception as e:
        LOGGER("PRINCEMUSIC").error(f"Error during shutdown: {e}")

def handle_exception(loop, context):
    """Global exception handler"""
    msg = context.get("exception", context["message"])
    LOGGER("PRINCEMUSIC").error(f"Unhandled exception: {msg}")

async def init():
    """Initialize the bot"""
    try:
        # Setup event loop
        loop = asyncio.get_running_loop()
        loop.set_exception_handler(handle_exception)

        # Setup signal handlers
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(
                sig,
                lambda s=sig: asyncio.create_task(shutdown(s, loop))
            )

        # Initialize aiohttp session
        await init_aiohttp_session()

        # Verify configurations
        if not all([config.API_ID, config.API_HASH, config.BOT_TOKEN, config.MONGO_DB_URI]):
            LOGGER("PRINCEMUSIC").error("Missing required configuration variables!")
            return False

        # Initialize the bot
        global app
        app = CustomClient(
            "PRINCEMUSIC",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN
        )

        # Start monitoring task
        TASKS.append(asyncio.create_task(monitor_resources()))

        # Initialize sudo users and banned users
        await sudo()
        
        try:
            users = await get_gbanned()
            for user_id in users:
                BANNED_USERS.add(user_id)
            users = await get_banned_users()
            for user_id in users:
                BANNED_USERS.add(user_id)
        except Exception as e:
            LOGGER("PRINCEMUSIC").error(f"Failed to load banned users: {e}")

        # Start the bot
        await app.start()
        
        # Load all modules
        await load_modules()
        LOGGER("PRINCEMUSIC.plugins").info("𝐀𝐥𝐥 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 𝐋𝐨𝐚𝐝𝐞𝐝 𝐁𝐚𝐛𝐲🥳...")

        # Start userbot and call client
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
            return False
        except Exception as e:
            LOGGER("PRINCEMUSIC").error(f"Stream call error: {e}")

        await PRINCE.decorators()
        LOGGER("PRINCEMUSIC").info(
            "╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎𝗠𝗔𝗗𝗘 𝗕𝗬 𝗠𝗥 𝗣𝗥𝗜𝗡𝗖𝗘\n╚═════ஜ۩۞۩ஜ════╝"
        )

        # Wait for commands
        await idle()
        return True

    except Exception as e:
        LOGGER("PRINCEMUSIC").error(f"Initialization error: {e}")
        return False

if __name__ == "__main__":
    try:
        if sys.platform.startswith('win'):
            policy = asyncio.WindowsSelectorEventLoopPolicy()
            asyncio.set_event_loop_policy(policy)
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        if loop.run_until_complete(init()):
            LOGGER("PRINCEMUSIC").info("Bot started successfully!")
        else:
            LOGGER("PRINCEMUSIC").error("Bot failed to start!")
            
    except KeyboardInterrupt:
        LOGGER("PRINCEMUSIC").info("Bot stopped by user!")
    except Exception as e:
        LOGGER("PRINCEMUSIC").error(f"Fatal error: {e}")
    finally:
        try:
            loop.run_until_complete(cleanup_resources())
        except:
            pass
        
        if loop.is_running():
            loop.stop()
        if not loop.is_closed():
            loop.close()
        
        gc.collect()
        sys.exit(0)
