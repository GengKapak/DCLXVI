import twitter_scraper
from requests import get
from userbot import CMD_HELP
from userbot.events import register

@register(pattern="^\.tw ?(.*)", outgoing=True)
async def twit(event):
    q = event.pattern_match.group(1)
    if len(q) < 1:
        await event.edit("`Please provide a Twitter account. Example: ``.tw username`")
        return
    try:
        twits = list(twitter_scraper.get_tweets(q, pages=1))
    except Exception as e:
        await event.edit(f"`Probably no such account. Because an error occurred. Error: {e}`")
        return

    if len(twits) > 2:
        if twits[0]["tweetId"] < twits[1]["tweetId"]:
            twit = twits[1]
            pic = twit['entries']['photos']
            result = []
            if len(pic) >= 1:
                i = 0
                while i < len(pic):
                    with open(f"{q}-{i}.jpg", 'wb') as load:
                        load.write(get(pic[i]).content)
                    result.append(f"{q}-{i}.jpg")
                    i += 1
                await event.client.send_file(event.chat_id, result, caption=f"**{q}**\n{twit['time']}\n\n`{twit['text']}`\n\n💬{twit['replies']} 🔁{twit['retweets']} ❤️{twit['likes']}")
                await event.delete()
                return
            await event.edit(f"**{q}**\n{twit['time']}\n\n`{twit['text']}`\n\n💬{twit['replies']} 🔁{twit['retweets']} ❤️{twit['likes']}")
        else:
            twit = twits[1]
            pic = twit['entries']['photos']
            result = []
            if len(pic) >= 1:
                i = 0
                while i < len(pic):
                    with open(f"{q}-{i}.jpg", 'wb') as load:
                        load.write(get(pic[i]).content)
                    result.append(f"{q}-{i}.jpg")
                    i += 1
                print(result)
                await event.client.send_file(event.chat_id, result, caption=f"**{q}**\n{twit['time']}\n\n`{twit['text']}`\n\n💬{twit['replies']} 🔁{twit['retweets']} ❤️{twit['likes']}")
                await event.delete()
                return
            await event.edit(f"**{q}**\n{twit['time']}\n\n`{twit['text']}`\n\n💬{twit['replies']} 🔁{twit['retweets']} ❤️{twit['likes']}")
        return
    else:
        twit = twits[0]
        pic = twit['entries']['photos']
        result = []
        if len(pic) >= 1:
            i = 0
            while i < len(pic):
                with open(f"{q}-{i}.jpg", 'wb') as load:
                    load.write(get(pic[i]).content)
                result.append(f"{q}-{i}.jpg")
                i += 1
            await event.client.send_file(event.chat_id, result, caption=f"**{q}**\n{twit['time']}\n\n`{twit['text']}`\n\n💬{twit['replies']} 🔁{twit['retweets']} ❤️{twit['likes']}")
            await event.delete()
            return
        await event.edit(f"**{q}**\n{twit['time']}\n\n`{twit['text']}`\n\n💬{twit['replies']} 🔁{twit['retweets']} ❤️{twit['likes']}")
        return

CMD_HELP.update({
    "twitter":
    ">`.tw` **username**"
    "\nUsage: Scrap latest tweet from someone."
})
