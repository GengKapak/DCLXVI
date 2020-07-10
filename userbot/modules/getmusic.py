import asyncio
import glob
import os
import subprocess

import requests
from bs4 import BeautifulSoup
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import CMD_HELP, bot
from userbot.events import register


# For song module
def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(
            seconds, 60) if count < 3 else divmod(
            seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "
    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time


def getmusic(get, DEFAULT_AUDIO_QUALITY):
    search = get

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    }

    html = requests.get(
        "https://www.youtube.com/results?search_query=" +
        search,
        headers=headers).text
    soup = BeautifulSoup(html, "html.parser")
    for link in soup.find_all("a"):
        if "/watch?v=" in link.get("href"):
            # May change when Youtube Website may get updated in the future.
            video_link = link.get("href")
            break

    video_link = "http://www.youtube.com/" + video_link
    command = (
        "youtube-dl --extract-audio --audio-format mp3 --audio-quality "
        + DEFAULT_AUDIO_QUALITY
        + " "
        + video_link
    )
    os.system(command)


@register(outgoing=True, pattern=r"^\.song (.*)")
async def _(event):
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
        await event.edit("`Wait..! I am finding your song..`")
    elif reply.message:
        query = reply.message
        await event.edit("`Wait..! I am finding your song..`")
    else:
        await event.edit("`What I am Supposed to find`")
        return

    getmusic(str(query), "320k")
    l = glob.glob("*.mp3")
    loa = l[0]
    await event.edit("`Yeah.. Uploading your song..`")
    await event.client.send_file(
        event.chat_id,
        loa,
        force_document=True,
        allow_cache=False,
        caption=query,
        reply_to=reply_to_id,
    )
    await event.delete()
    os.system("rm -rf *.mp3")
    subprocess.check_output("rm -rf *.mp3", shell=True)


@register(outgoing=True, pattern=r"^\.smd(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    chat = "@SpotifyMusicDownloaderBot"
    await event.edit("```Getting Your Music```")
    async with bot.conversation(chat) as conv:
        await asyncio.sleep(2)
        await event.edit("`Downloading music taking some times,  Stay Tuned.....`")
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=752979930)
            )
            await bot.send_message(chat, link)
            respond = await response
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await event.reply(
                "```Please unblock @SpotifyMusicDownloaderBot and try again```"
            )
            return
        await event.delete()
        await bot.forward_messages(event.chat_id, respond.message)
        await bot.send_read_acknowledge(event.chat_id)


@register(outgoing=True, pattern=r"^\.net(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    song = event.pattern_match.group(1)
    chat = "@WooMaiBot"
    link = f"/netease {song}"
    await event.edit("```Getting Your Music```")
    async with bot.conversation(chat) as conv:
        await asyncio.sleep(2)
        await event.edit("`Downloading...Please wait`")
        try:
            msg = await conv.send_message(link)
            response = await conv.get_response()
            respond = await conv.get_response()
            """ - don't spam notif - """
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await event.reply("```Please unblock @WooMaiBot and try again```")
            return
        await event.edit("`Sending Your Music...`")
        await asyncio.sleep(3)
        await bot.send_file(event.chat_id, respond)
    await event.client.delete_messages(conv.chat_id, [msg.id, response.id, respond.id])
    await event.delete()


@register(outgoing=True, disable_errors=True, pattern=r"^\.sdd(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    d_link = event.pattern_match.group(1)
    if ".com" not in d_link:
        await event.edit("` I need a link to download something pro.`**(._.)**")
    else:
        await event.edit("**Initiating Download!**")
    chat = "@MusicHuntersBot"
    async with bot.conversation(chat) as conv:
        try:
            msg_start = await conv.send_message("/start")
            response = await conv.get_response()
            msg = await conv.send_message(d_link)
            details = await conv.get_response()
            song = await conv.get_response()
            """ - don't spam notif - """
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await event.edit("**Error:** `unblock` @MusicHuntersBot `and retry!`")
            return
        await bot.send_file(event.chat_id, song, caption=details.text)
        await event.client.delete_messages(
            conv.chat_id, [msg_start.id, response.id, msg.id, details.id, song.id]
        )
        await event.delete()


CMD_HELP.update(
    {
        "song": ">`.song` **Artist - Song Title**"
        "\nUsage: Finding and uploading song.\n"
        ">`.smd` **Artist - Song Title**"
        "\nUsage: Download music from spotify.\n"
        ">`.net` **Artist - Song Title**"
        "\nUsage: Download music with @WooMaiBot.\n"
        ">`.sdd <Spotify/Deezer Link>`"
        "\nUsage: Download music from Spotify or Deezer."
    }
)
