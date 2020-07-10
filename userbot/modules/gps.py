# Copyright (C) 2020 GengKapak and AnggaR96s.
# All rights reserved.
from geopy.geocoders import Nominatim
from telethon.tl import types

from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern=r"^\.gps (.*)")
async def gps(e):
    if e.fwd_from:
        return
    reply_to_id = e.message.id
    if e.reply_to_msg_id:
        reply_to_id = e.reply_to_msg_id
    input_str = e.pattern_match.group(1)

    if not input_str:
        return await e.edit("`What should i find give me location.`")

    await e.edit("`Finding`")

    geolocator = Nominatim(user_agent="GengKapak")
    geoloc = geolocator.geocode(input_str)
    if geoloc:
        lon = geoloc.longitude
        lat = geoloc.latitude
        await e.reply(
            input_str,
            file=types.InputMediaGeoPoint(types.InputGeoPoint(lat, lon)),
            reply_to=reply_to_id,
        )
        await e.delete()
    else:
        await e.edit("`I coudn't find it.`")


CMD_HELP.update({"gps": ">`.gps` **Location**" "\nUsage: Search location."})
