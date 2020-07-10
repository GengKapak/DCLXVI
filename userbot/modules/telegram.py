# fix by @heyworld for OUB
# bug fixed by @d3athwarrior
from telethon.tl.types import InputMediaDice

from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern=r"^\.dice(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.delete()
    r = await event.reply(file=InputMediaDice(""))
    if input_str:
        try:
            required_number = int(input_str)
            while r.media.value != required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice(""))
        except BaseException:
            pass


@register(outgoing=True, pattern=r"^\.dart(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.delete()
    r = await event.reply(file=InputMediaDice("🎯"))
    if input_str:
        try:
            required_number = int(input_str)
            while r.media.value != required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice("🎯"))
        except BaseException:
            pass


@register(outgoing=True, pattern=r"^\.ball(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.delete()
    r = await event.reply(file=InputMediaDice("🏀"))
    if input_str:
        try:
            required_number = int(input_str)
            while r.media.value != required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice("🏀"))
        except BaseException:
            pass


CMD_HELP.update(
    {
        "dice": ">`.dice` or .dice 1 to 6 any value\
\nUsage: hahaha just a magic.\
\nwarning: `you would be in trouble if you input any other value than mentioned.`"
    }
)

CMD_HELP.update(
    {
        "basketball": ">`.ball` or .ball 1 to 5 any value\
\nUsage: hahaha just a magic.\
\nwarning: `you would be in trouble if you input any other value than mentioned.`"
    }
)

CMD_HELP.update(
    {
        "dart": ">`.dart` or .dart 1 to 6 any value\
\nUsage: hahaha just a magic.\
\nwarning: `you would be in trouble if you input any other value than mentioned.`"
    }
)
