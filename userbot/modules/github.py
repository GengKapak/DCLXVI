import aiohttp

from userbot import CMD_HELP
from userbot.events import register


@register(pattern=r"^\.git (.*)", outgoing=True)
async def github(event):
    URL = f"https://api.github.com/users/{event.pattern_match.group(1)}"
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as request:
            if request.status == 404:
                return await event.reply(
                    "`" + event.pattern_match.group(1) + " not found`"
                )

            result = await request.json()

            url = result.get("html_url", None)
            name = result.get("name", None)
            company = result.get("company", None)
            blog = result.get("blog", None)
            loc = result.get("location", None)
            email = result.get("email", None)
            bio = result.get("bio", None)
            twitter = result.get("twitter_username", None)
            repo = result.get("public_repos", None)
            gist = result.get("public_gists", None)
            followers = result.get("followers", None)
            following = result.get("following", None)
            created_at = result.get("created_at", "Not Found")

            REPLY = (
                f"GitHub Info for `{event.pattern_match.group(1)}`"
                f"\nUsername: `{name}`"
                f"\nURL: {url}"
                f"\nTwitter: https://twitter.com/{twitter}"
                f"\nBlog: {blog}"
                f"\nBio: `{bio}`"
                f"\nLocation: `{loc}`"
                f"\nEmail: {email}"
                f"\nCompany: `{company}`"
                f"\nPublic Repos: `{repo}`"
                f"\nPublic Gists: `{gist}`"
                f"\nFollowers: `{followers}`"
                f"\nFollowing: `{following}`"
                f"\nCreated at: `{created_at}`"
            )

            if not result.get("repos_url", None):
                return await event.edit(REPLY)
            async with session.get(result.get("repos_url", None)) as request:
                result = request.json
                if request.status == 404:
                    return await event.edit(REPLY)

                result = await request.json()

                REPLY += "\nRepos:\n"

                for nr in range(len(result)):
                    REPLY += f"[{result[nr].get('name', None)}]({result[nr].get('html_url', None)})\n"

                await event.edit(REPLY)


CMD_HELP.update({"git": ">`.git <username>`"
                 "\nUsage: Like .whois but for GitHub usernames."})
