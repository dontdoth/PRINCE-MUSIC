from pyrogram import Client, enums, filters
from PRINCEMUSIC import app as app
from pyrogram.handlers import MessageHandler

@app.on_message(filters.command("تاس"))
async def dice(bot, message):
    x=await bot.send_dice(message.chat.id)
    m=x.dice.value
    await message.reply_text(f"سلام {message.from_user.mention} امتیاز شما : {m}",quote=True)
  
@app.on_message(filters.command("دارت")) 
async def dart(bot, message):
    x=await bot.send_dice(message.chat.id, "🎯")
    m=x.dice.value
    await message.reply_text(f"سلام {message.from_user.mention} امتیاز شما : {m}",quote=True)

@app.on_message(filters.command("بسکتبال"))
async def basket(bot, message):
    x=await bot.send_dice(message.chat.id, "🏀")
    m=x.dice.value
    await message.reply_text(f"سلام {message.from_user.mention} امتیاز شما : {m}",quote=True)

@app.on_message(filters.command("اسلات"))
async def jackpot(bot, message):
    x=await bot.send_dice(message.chat.id, "🎰")
    m=x.dice.value
    await message.reply_text(f"سلام {message.from_user.mention} امتیاز شما : {m}",quote=True)

@app.on_message(filters.command("بولینگ"))
async def bowling(bot, message):
    x=await bot.send_dice(message.chat.id, "🎳")
    m=x.dice.value
    await message.reply_text(f"سلام {message.from_user.mention} امتیاز شما : {m}",quote=True)

@app.on_message(filters.command("فوتبال"))
async def football(bot, message):
    x=await bot.send_dice(message.chat.id, "⚽")
    m=x.dice.value
    await message.reply_text(f"سلام {message.from_user.mention} امتیاز شما : {m}",quote=True)

__mod_name__ = "بازی‌ها"
