import os
import random
import time

from pyrogram import Client
from pyrogram.types import Message

from Pbxbot import START_TIME
from Pbxbot.core import ENV
from Pbxbot.functions.formatter import readable_time
from Pbxbot.functions.images import generate_alive_image
from Pbxbot.functions.templates import alive_template, ping_template

from . import Config, HelpMenu, db, Pbxbot, on_message


@on_message("alive", allow_stan=True)
async def alive(client: Client, message: Message):
    Pbx = await Pbxbot.edit(message, "ʀᴜᴋᴏ ʙᴀʙʏ ☹️✨❤️")

    img = await db.get_env(ENV.alive_pic)
    if not img:
        if message.from_user.photo:
            user_pfp = await client.download_media(message.from_user.photo.big_file_id)
            del_path = True
        else:
            user_pfp = "./Pbxbot/resources/images/Pbxbot_logo.png"
            del_path = False
        img = [
            generate_alive_image(
                message.from_user.first_name, user_pfp, del_path, Config.FONT_PATH
            )
        ]
    else:
        img = img.split(" ")

    img = random.choice(img)
    uptime = readable_time(time.time() - START_TIME)
    caption = await alive_template(client.me.first_name, uptime)

    if img.endswith(".mp4"):
        await message.reply_video(img, caption=caption)
    else:
        await message.reply_photo(img, caption=caption)
    await Pbx.delete()

    try:
        os.remove(img)
    except:
        pass


@on_message("ping", allow_stan=True)
async def ping(client: Client, message: Message):
    start_time = time.time()
    Pbx = await Pbxbot.edit(message, "`·.·★ AᴜJʟᴀ 2.0 ★·.·´")
    uptime = readable_time(time.time() - START_TIME)
    img = await db.get_env(ENV.ping_pic)
    end_time = time.time()
    speed = end_time - start_time
    caption = await ping_template(round(speed, 3), uptime, client.me.mention)
    if img:
        PIC = "https://te.legra.ph/file/0575d74af6385a5c9d3a4.jpg"
        img = random.choice(img.split(" "))
        if img.endswith(".mp4"):
            await message.reply_video(
                img,
                caption=caption,
            )
        else:
            await message.reply_photo(
                img,
                caption=caption,
            )
        return
    await Pbxbot.edit(Pbx, caption, no_link_preview=True)


@on_message("history", allow_stan=True)
async def history(client: Client, message: Message):
    if not message.reply_to_message:
        if len(message.command) < 2:
            return await Pbxbot.delete(
                message, "Either reply to an user or give me a username to get history."
            )
        try:
            user = await client.get_users(message.command[1])
        except Exception as e:
            return await Pbxbot.error(message, f"`{str(e)}`")
    else:
        user = message.reply_to_message.from_user

    Pbx = await Pbxbot.edit(message, "Processing ...")

    try:
        response = await client.ask("@SangMata_BOT", f"{user.id}", timeout=60)
    except Exception as e:
        return await Pbxbot.error(Pbx, f"`{str(e)}`")

    if "you have used up your quota for today" in response.text:
        return await Pbxbot.delete(
            Pbx,
            f"Your quota of using SangMata Bot is over. Wait till 00:00 UTC before using it again.",
        )

    try:
        await response.delete()
        await response.request.delete()
    except:
        pass

    await Pbxbot.edit(Pbx, response.text)


HelpMenu("bot").add(
    "alive",
    None,
    "Get the alive message of the bot.",
    "alive",
    "You can also customize alive message with suitable variables for it.",
).add(
    "ping",
    None,
    "Check the ping speed and uptime of bot.",
    "ping",
    "You can also customize ping message by adding a media to it.",
).add(
    "history",
    "<reply to user>/<username/id>",
    "Get the username, name history of an user.",
    "history @PB65_Aujla",
    "This command uses SangMata Bot to get the history.",
).info(
    "Alive Menu"
).done()
