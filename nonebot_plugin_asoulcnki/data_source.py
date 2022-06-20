import time
import httpx
import jinja2
import random
from pathlib import Path
from typing import Union, Dict, Any

from nonebot_plugin_htmlrender import html_to_pic
from nonebot.adapters.onebot.v11 import Message, MessageSegment

from .diff import diff_text

dir_path = Path(__file__).parent
template_path = dir_path / "templates"
env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_path), enable_async=True
)


async def check_text(text: str) -> Union[str, Message]:
    url = "https://asoulcnki.asia/v1/api/check"
    async with httpx.AsyncClient() as client:
        resp = await client.post(url=url, json={"text": text})
        resp.raise_for_status()
        result = resp.json()

    data = result["data"]
    if not data["related"]:
        return "没有找到重复的小作文捏"

    rate = data["rate"]
    related = data["related"][0]
    reply_url = str(related["reply_url"]).strip()
    reply = related["reply"]

    image = await render_reply(reply, diff=text)

    msg = Message()
    msg.append("总复制比 {:.2f}%".format(rate * 100))
    msg.append(MessageSegment.image(image))
    msg.append(f"链接：{reply_url}")
    return msg


async def random_text(keyword: str = "") -> Union[str, Message]:
    url = "https://asoulcnki.asia/v1/api/ranking"
    params: Dict[str, Any] = {
        "pageSize": 10,
        "pageNum": 1,
        "timeRangeMode": 0,
        "sortMode": 0,
    }
    if keyword:
        params["keywords"] = keyword
    else:
        params["pageNum"] = random.randint(1, 100)

    async with httpx.AsyncClient() as client:
        resp = await client.get(url=url, params=params)
        resp.raise_for_status()
        result = resp.json()

    replies = result["data"]["replies"]
    if not replies:
        return "没有找到小作文捏"

    reply = random.choice(replies)
    image = await render_reply(reply)

    reply_url = f"https://t.bilibili.com/{reply['dynamic_id']}/#reply{reply['rpid']}"
    msg = Message()
    msg.append(MessageSegment.image(image))
    msg.append(f"链接：{reply_url}")
    return msg


async def render_reply(reply: dict, diff: str = "") -> bytes:
    article = {}
    article["username"] = reply["m_name"]
    article["like"] = reply["like_num"]
    article["all_like"] = reply["similar_like_sum"]
    article["quote"] = reply["similar_count"]
    article["text"] = diff_text(diff, reply["content"]) if diff else reply["content"]
    article["time"] = time.strftime("%Y-%m-%d", time.localtime(reply["ctime"]))

    template = env.get_template("article.html")
    html = await template.render_async(article=article)
    return await html_to_pic(html, wait=0, viewport={"width": 500, "height": 100})
