from pyrogram import Client
from pyrogram.dispatcher import Dispatcher
import asyncio
import logging
from typing import List, Dict
from collections import defaultdict

LOGGER = logging.getLogger(__name__)

class CustomDispatcher(Dispatcher):
    def __init__(self, client: Client, workers: int = 4, *args, **kwargs):
        super().__init__(client, workers, *args, **kwargs)
        self.running_tasks: Dict[str, List[asyncio.Task]] = defaultdict(list)
        self._shutdown = asyncio.Event()

    async def start(self):
        """Start the dispatcher"""
        for i in range(self.workers):
            self.tasks.append(
                asyncio.create_task(
                    self.handler_worker(f"Handler-{i+1}"),
                    name=f"Handler-{i+1}"
                )
            )
        LOGGER.info(f"Started {self.workers} HandlerTasks")

    async def stop(self):
        """Stop the dispatcher"""
        self._shutdown.set()
        
        # Cancel all running tasks
        for task_list in self.running_tasks.values():
            for task in task_list:
                if not task.done():
                    task.cancel()
                    try:
                        await task
                    except asyncio.CancelledError:
                        pass
                    except Exception as e:
                        LOGGER.error(f"Error while cancelling task: {e}")

        # Clear running tasks
        self.running_tasks.clear()

        # Stop handler workers
        for task in self.tasks:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            except Exception as e:
                LOGGER.error(f"Error while stopping handler: {e}")

        self.tasks.clear()
        self.groups.clear()
        self.updates_queue.clear()
        LOGGER.info("Dispatcher stopped")

    async def handler_worker(self, name: str):
        """Handler worker task"""
        while not self._shutdown.is_set():
            try:
                update = await self.updates_queue.get()
                if update is None:
                    break

                task = asyncio.create_task(
                    self.process_update(update),
                    name=f"Process-{update.update_id}"
                )
                self.running_tasks[name].append(task)
                
                # Cleanup finished tasks
                self.running_tasks[name] = [
                    t for t in self.running_tasks[name] if not t.done()
                ]

            except asyncio.CancelledError:
                break
            except Exception as e:
                LOGGER.error(f"Error in handler worker {name}: {e}")
                await asyncio.sleep(1)

    async def process_update(self, update):
        """Process single update"""
        try:
            await super().process_update(update)
        except Exception as e:
            LOGGER.error(f"Error processing update {update.update_id}: {e}")
