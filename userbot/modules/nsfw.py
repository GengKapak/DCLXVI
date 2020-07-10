# Credits to https://t.me/TheHardGamer
# Edited by @AnggaR96s
import os
import urllib
from asyncio import sleep

import requests

from userbot import CMD_HELP, bot
from userbot.events import register


@register(outgoing=True, pattern=r"^\.boobs(?: |$)(.*)")
async def boobs(e):
    await e.edit("`Finding some big boobs...`")
    await sleep(3)
    await e.edit("`Sending some big boobs...`")
    nsfw = requests.get("http://api.oboobs.ru/noise/1").json()[0]["preview"]
    urllib.request.urlretrieve(
        "http://media.oboobs.ru/{}".format(nsfw), "*.jpg")
    os.rename("*.jpg", "boobs.jpg")
    await bot.send_file(e.chat_id, "boobs.jpg")
    os.remove("boobs.jpg")
    await e.delete()


@register(outgoing=True, pattern=r"^\.butts(?: |$)(.*)")
async def butts(e):
    await e.edit("`Finding some beautiful butts...`")
    await sleep(3)
    await e.edit("`Sending some beautiful butts...`")
    nsfw = requests.get("http://api.obutts.ru/noise/1").json()[0]["preview"]
    urllib.request.urlretrieve(
        "http://media.obutts.ru/{}".format(nsfw), "*.jpg")
    os.rename("*.jpg", "butts.jpg")
    await bot.send_file(e.chat_id, "butts.jpg")
    os.remove("butts.jpg")
    await e.delete()


CMD_HELP.update(
    {
        "nsfw": ">`.boobs`"
        "\nUsage: Get boobs image.\n"
        ">`.butts`"
        "\nUsage: Get butts image."
    }
)
