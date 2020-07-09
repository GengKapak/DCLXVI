import asyncio
import datetime
import html
import textwrap

import bs4
import requests
from jikanpy import Jikan
from jikanpy.exceptions import APIException
from userbot import CMD_HELP
from userbot.events import register

jikan = Jikan()


@register(outgoing=True, pattern=r"^\.anime ?(.*)")
async def anime(event):
    query = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    await event.edit("`Searching Anime...`")
    if query:
        pass
    elif reply:
        query = reply.text
    else:
        await event.edit("`Bruh.. What I am supposed to search ?`")
        await asyncio.sleep(6)
        await event.delete()
        return
    try:
        res = jikan.search("anime", query)
    except Exception as err:
        await event.edit(f"**Error:** \n`{err}`")
        return
    try:
        res = res.get("results")[0].get("mal_id")  # Grab first result
    except APIException:
        await event.edit("`Error connecting to the API. Please try again!`")
        return
    if res:
        anime = jikan.anime(res)
        title = anime.get("title")
        japanese = anime.get("title_japanese")
        eng_title = anime.get("title_english")
        type = anime.get("type")
        duration = anime.get("duration")
        synopsis = anime.get("synopsis")
        source = anime.get("source")
        status = anime.get("status")
        episodes = anime.get("episodes")
        score = anime.get("score")
        rating = anime.get("rating")
        genre_lst = anime.get("genres")
        genres = ""
        for genre in genre_lst:
            genres += genre.get("name") + ", "
        genres = genres[:-2]
        studios = ""
        studio_lst = anime.get("studios")
        for studio in studio_lst:
            studios += studio.get("name") + ", "
        studios = studios[:-2]
        duration = anime.get("duration")
        premiered = anime.get("premiered")
        image_url = anime.get("image_url")
        trailer = anime.get("trailer_url")
        if trailer:
            bru = f"<a href='{trailer}'>Trailer</a>"
        else:
            bru = "<code>No Trailer Available</code>"
        url = anime.get("url")
    else:
        await event.edit("`No results Found!`")
        return
    rep = f"<b>{title}</b> - ({japanese})\n"
    rep += f"<b>Type:</b> <code>{type}</code>\n"
    rep += f"<b>Source:</b> <code>{source}</code>\n"
    rep += f"<b>Status:</b> <code>{status}</code>\n"
    rep += f"<b>Genres:</b> <code>{genres}</code>\n"
    rep += f"<b>Episodes:</b> <code>{episodes}</code>\n"
    rep += f"<b>Duration:</b> <code>{duration}</code>\n"
    rep += f"<b>Score:</b> <code>{score}</code>\n"
    rep += f"<b>Studio(s):</b> <code>{studios}</code>\n"
    rep += f"<b>Premiered:</b> <code>{premiered}</code>\n"
    rep += f"<b>Rating:</b> <code>{rating}</code>\n\n"
    rep += f"<a href='{image_url}'>\u200c</a>"
    rep += f"📖 <b>Synopsis</b>: <i>{synopsis}</i>\n"
    rep += f'<b>Read More:</b> <a href="{url}">MyAnimeList</a>'
    await event.edit(rep, parse_mode="HTML", link_preview=False)


@register(outgoing=True, pattern=r"^\.manga ?(.*)")
async def manga(event):
    query = event.pattern_match.group(1)
    await event.edit("`Searching Manga...`")
    if not query:
        await event.edit("`Bruh.. Gib me Something to Search`")
        return
    res = ""
    manga = ""
    try:
        res = jikan.search("manga", query).get("results")[0].get("mal_id")
    except APIException:
        await event.edit("`Error connecting to the API. Please try again!`")
        return ""
    if res:
        try:
            manga = jikan.manga(res)
        except APIException:
            await event.edit("`Error connecting to the API. Please try again!`")
            return ""
        title = manga.get("title")
        japanese = manga.get("title_japanese")
        type = manga.get("type")
        status = manga.get("status")
        score = manga.get("score")
        volumes = manga.get("volumes")
        chapters = manga.get("chapters")
        genre_lst = manga.get("genres")
        genres = ""
        for genre in genre_lst:
            genres += genre.get("name") + ", "
        genres = genres[:-2]
        synopsis = manga.get("synopsis")
        image = manga.get("image_url")
        url = manga.get("url")
        rep = f"<b>{title} ({japanese})</b>\n"
        rep += f"<b>Type:</b> <code>{type}</code>\n"
        rep += f"<b>Status:</b> <code>{status}</code>\n"
        rep += f"<b>Genres:</b> <code>{genres}</code>\n"
        rep += f"<b>Score:</b> <code>{score}</code>\n"
        rep += f"<b>Volumes:</b> <code>{volumes}</code>\n"
        rep += f"<b>Chapters:</b> <code>{chapters}</code>\n\n"
        rep += f"<a href='{image}'>\u200c</a>"
        rep += f"📖 <b>Synopsis</b>: <i>{synopsis}</i>\n"
        rep += f'<b>Read More:</b> <a href="{url}">MyAnimeList</a>'
        await event.edit(rep, parse_mode="HTML", link_preview=False)


@register(outgoing=True, pattern=r"^\.a(kaizoku|kayo) ?(.*)")
async def site_search(event):
    message = await event.get_reply_message()
    search_query = event.pattern_match.group(2)
    site = event.pattern_match.group(1)
    if search_query:
        pass
    elif message:
        search_query = message.text
    else:
        await event.edit("`Uuf Bro.. Gib something to Search`")
        return

    if site == "kaizoku":
        search_url = f"https://animekaizoku.com/?s={search_query}"
        html_text = requests.get(search_url).text
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h2", {"class": "post-title"})

        if search_result:
            result = f"<a href='{search_url}'>Click Here For More Results</a> <b>of</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKaizoku</code>: \n\n"
            for entry in search_result:
                post_link = entry.a["href"]
                post_name = html.escape(entry.text.strip())
                result += f"• <a href='{post_link}'>{post_name}</a>\n"
                await event.edit(result, parse_mode="HTML")
        else:
            result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKaizoku</code>"
            await event.edit(result, parse_mode="HTML")

    elif site == "kayo":
        search_url = f"https://animekayo.com/?s={search_query}"
        html_text = requests.get(search_url).text
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h2", {"class": "title"})

        result = f"<a href='{search_url}'>Click Here For More Results</a> <b>of</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKayo</code>: \n\n"
        for entry in search_result:

            if entry.text.strip() == "Nothing Found":
                result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKayo</code>"
                break

            post_link = entry.a["href"]
            post_name = html.escape(entry.text.strip())
            result += f"• <a href='{post_link}'>{post_name}</a>\n"
            await event.edit(result, parse_mode="HTML")


@register(outgoing=True, pattern=r"^\.upcoming ?(.*)")
async def upcoming(message):
    rep = "<b>Upcoming anime</b>\n"
    later = jikan.season_later()
    anime = later.get("anime")
    for new in anime:
        name = new.get("title")
        url = new.get("url")
        rep += f"• <a href='{url}'>{name}</a>\n"
        if len(rep) > 1000:
            break
        await message.edit(rep, parse_mode="html")


CMD_HELP.update(
    {
        "anime": ">`.anime <anime>` Returns with Anime information.\n"
        ">`.manga <manga name>` Returns with the Manga information.\n"
        ">`.akaizoku` or `.akayo` <anime name> Returns with the Anime Downlaod link.\n"
        ">`.upcoming` Returns with Upcoming Anime information."
    }
)
