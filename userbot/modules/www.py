# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing commands related to the \
    Information Superhighway (yes, Internet). """

import os
import wget
from datetime import datetime
from speedtest import Speedtest
from telethon import functions
from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern="^\.speed$")
async def speedtst(spd):
    """ For .speed command, use SpeedTest to check server speeds. """
    await spd.edit("`Running speed test . . .`")
    test = Speedtest()

    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()
    path = wget.download(result['share'])
    output =  f"""**
                Started at `{result['timestamp']}`

		Client:

		ISP: `{result['client']['isp']}`
		Country: `{result['client']['country']}`

		Server:
		Name: `{result['server']['name']}`
		Country: `{result['server']['country']}, {result['server']['cc']}`
		Sponsor: `{result['server']['sponsor']}`
		Latency: `{result['server']['latency']}`

		Ping: `{result['ping']}`
		Sent: `{humanbytes(result['bytes_sent'])}`
		Received: `{humanbytes(result['bytes_received'])}`
		Download: `{humanbytes(result['download'] / 8)}/s`
		Upload: `{humanbytes(result['upload'] / 8)}/s`**"""
    await spd.delete()
    await spd.client.send_file(spd.chat_id,
                                   path,
                                   caption=output,
                                   force_document=False)
    os.remove(path)


def humanbytes(size: float) -> str:
    """humanize size"""
    if not size:
        return ""
    power = 1024
    t_n = 0
    power_dict = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        t_n += 1
    return "{:.2f} {}B".format(size, power_dict[t_n])


@register(outgoing=True, pattern="^\.dc$")
async def neardc(event):
    """ For .dc command, get the nearest datacenter information. """
    result = await event.client(functions.help.GetNearestDcRequest())
    await event.edit(f"Country : `{result.country}`\n"
                     f"Nearest Datacenter : `{result.nearest_dc}`\n"
                     f"This Datacenter : `{result.this_dc}`")


@register(outgoing=True, pattern="^\.ping$")
async def pingme(pong):
    """ For .ping command, ping the userbot from any chat.  """
    start = datetime.now()
    await pong.edit("`Pong!`")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await pong.edit("`Pong!\n%sms`" % (duration))


CMD_HELP.update({
     "speed":
     ">`.speed`"
     "\nUsage: Does a speedtest and shows the results.",
     "dc":
     ">`.dc`"
     "\nUsage: Finds the nearest datacenter from your server.",
     "ping":
     ">`.ping`"
     "\nUsage: Shows how long it takes to ping your bot."
})
