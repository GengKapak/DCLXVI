# Credits to https://t.me/TheHardGamer
# Edited by @AnggaR96s

import datetime
from telethon import events
import io
import os
import urllib
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import re
from telethon.tl.types import MessageMediaPhoto
from PIL import Image
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from userbot import bot, CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern="^.boobs(?: |$)(.*)")
async def boobs(e):
    nsfw = requests.get('http://api.oboobs.ru/noise/1').json()[0]["preview"]
    urllib.request.urlretrieve("http://media.oboobs.ru/{}".format(nsfw), "*.jpg")
    os.rename('*.jpg', 'boobs.jpg')
    await bot.send_file(e.chat_id, "boobs.jpg")
    os.remove("boobs.jpg")
    await e.delete()

@register(outgoing=True, pattern="^.butts(?: |$)(.*)")
async def butts(e):
    nsfw = requests.get('http://api.obutts.ru/noise/1').json()[0]["preview"]
    urllib.request.urlretrieve("http://media.obutts.ru/{}".format(nsfw), "*.jpg")
    os.rename('*.jpg', 'butts.jpg')
    await bot.send_file(e.chat_id, "butts.jpg")
    os.remove("butts.jpg")
    await e.delete()

CMD_HELP.update({
    'nsfw':
    ">`.boobs`"
    "\nUsage: Get boobs image.\n"
    ">`.butts`"
    "\nUsage: Get butts image."
})
