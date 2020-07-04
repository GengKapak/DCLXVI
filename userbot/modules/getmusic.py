from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
import asyncio
from userbot.events import register
from userbot import bot, CMD_HELP


@register(outgoing=True, pattern="^\.smd(?: |$)(.*)")
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
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=752979930))
              await bot.send_message(chat, link)
              respond = await response
              await bot.send_read_acknowledge(conv.chat_id)
          except YouBlockedUserError:
              await event.reply("```Please unblock @SpotifyMusicDownloaderBot and try again```")
              return
          await event.delete()
          await bot.forward_messages(event.chat_id, respond.message)
          await bot.send_read_acknowledge(event.chat_id)

@register(outgoing=True, pattern="^\.net(?: |$)(.*)")
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
    await event.client.delete_messages(conv.chat_id,
                                       [msg.id, response.id, respond.id])
    await event.delete()

@register(outgoing=True, disable_errors=True, pattern="^\.sdd(?: |$)(.*)")
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
          await event.client.delete_messages(conv.chat_id,
                                             [msg_start.id, response.id, msg.id, details.id, song.id])
          await event.delete()

CMD_HELP.update({
    "song":
        ">`.smd` **Artist - Song Title**"
        "\nUsage: Download music from spotify.\n"
        ">`.net` **Artist - Song Title**"
        "\nUsage: Download music with @WooMaiBot.\n"
        ">`.sdd <Spotify/Deezer Link>`"
        "\nUsage: Download music from Spotify or Deezer."
})
