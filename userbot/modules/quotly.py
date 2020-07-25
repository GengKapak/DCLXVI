# Copyright (C) 2018-2019 Friendly Telegram
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# Port to UserBot by @MoveAngel

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import CMD_HELP, bot
from userbot.events import register


@register(outgoing=True, pattern=r"^\.q(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("`Reply to chat.`")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.text:
        await event.edit("`It's not a text!`")
        return
    chat = "@QuotLyBot"
    await event.edit("```Making a Quote```")
    async with bot.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=1031952739)
            )
            msg = await bot.forward_messages(chat, reply_message)
            response = await response
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await event.reply("```Please unblock @QuotLyBot and try again```")
            return
        if response.text.startswith("Hi!"):
            await event.edit(
                "`Can you kindly disable your forward privacy settings for good?`"
            )
        else:
            await event.delete()
            await bot.forward_messages(event.chat_id, response.message)
            await bot.send_read_acknowledge(event.chat_id)
            await event.client.delete_messages(conv.chat_id, [msg.id, response.id])


CMD_HELP.update(
    {"quotly": ">`.q` Reply to chat." "\nUsage: Enhance ur text to sticker.\n"}
)
