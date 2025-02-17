import gc
from pyrogram import Client
from ..logging import LOGGER
import config
import asyncio

assistants = []
assistantids = []

class Userbot(Client):
    def __init__(self):
        self._clients = {}
        self._active_calls = set()
        self._memory_usage = 0

    async def _start_client(self, name, session, number):
        try:
            client = Client(
                name=name,
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                session_string=str(session),
                no_updates=True,
                in_memory=True
            )
            
            await client.start()
            
            try:
                await client.join_chat("atrinmusic_tm")
                await client.join_chat("atrinmusic_tm1")
            except Exception as e:
                LOGGER(__name__).warning(f"Failed to join channels for {name}: {e}")
            
            try:
                await client.send_message(config.LOGGER_ID, f"Assistant {number} Started")
            except Exception as e:
                LOGGER(__name__).error(f"Failed to send startup message for {name}: {e}")
            
            client.id = client.me.id
            client.name = client.me.mention
            client.username = client.me.username
            
            assistants.append(number)
            assistantids.append(client.id)
            
            LOGGER(__name__).info(f"Assistant {number} Started as {client.name}")
            return client
            
        except Exception as e:
            LOGGER(__name__).error(f"Failed to start {name}: {e}")
            return None

    async def start(self):
        LOGGER(__name__).info("Starting Assistants...")
        
        sessions = [
            ("PRINCEAss1", config.STRING1, 1),
            ("PRINCEAss2", config.STRING2, 2),
            ("PRINCEAss3", config.STRING3, 3),
            ("PRINCEAss4", config.STRING4, 4),
            ("PRINCEAss5", config.STRING5, 5)
        ]
        
        for name, session, number in sessions:
            if session:
                client = await self._start_client(name, session, number)
                if client:
                    self._clients[number] = client
        
        if not self._clients:
            LOGGER(__name__).error("No assistants could be started!")
            return False
            
        return True

    async def stop(self):
        LOGGER(__name__).info("Stopping Assistants...")
        for client in self._clients.values():
            try:
                await client.stop()
            except Exception as e:
                LOGGER(__name__).error(f"Error stopping client: {e}")
        
        self._clients.clear()
        gc.collect()

    async def cleanup(self):
        """Periodic cleanup of resources"""
        while True:
            try:
                # Clear inactive calls
                current_time = asyncio.get_event_loop().time()
                inactive_calls = {
                    call for call in self._active_calls 
                    if current_time - call.last_activity > 300  # 5 minutes
                }
                for call in inactive_calls:
                    await call.stop()
                self._active_calls -= inactive_calls

                # Force garbage collection
                gc.collect()

                await asyncio.sleep(config.CLEANUP_INTERVAL)
            except Exception as e:
                LOGGER(__name__).error(f"Cleanup error: {e}")
                await asyncio.sleep(60)
