import json
import time
import httpx
import jinja2
import pkgutil
from nonebot.log import logger
from nonebot.adapters.cqhttp import Message, MessageSegment

from .browser import get_new_page
from .diff import diff_text

env = jinja2.Environment(enable_async=True)
article_data = pkgutil.get_data(__name__, "templates/article.html").decode()
article_tpl = env.from_string(article_data)


async def check_text(text) -> Message:
    try:
        url = 'https://asoulcnki.asia/v1/api/check'
        async with httpx.AsyncClient() as client:
            resp = await client.post(url=url, data=json.dumps({'text': text}))
            result = resp.json()

        code = result['code']
        if code != 0:
            return None

        data = result['data']
        if not data['related']:
            return '没有找到重复的小作文捏'

        rate = data['rate']
        related = data['related'][0]
        reply_url = related['reply_url'].strip()
        reply = related['reply']
        ctime = reply['ctime']

        article = {}
        article['username'] = reply['m_name']
        article['like'] = reply['like_num']
        article['all_like'] = reply['similar_like_sum']
        article['quote'] = reply['similar_count']
        article['text'] = diff_text(text, reply['content'])
        article['time'] = time.strftime("%Y-%m-%d", time.localtime(ctime))

        image = await create_image(article)
        if not image:
            return None

        msg = Message()
        msg.append('总复制比 {:.2f}%'.format(rate * 100))
        msg.append(MessageSegment.image(image))
        msg.append(f'链接：{reply_url}')
        return msg
    except Exception as e:
        logger.warning(f"Error in check_text: {e}")
        return None


async def create_image(article) -> bytes:
    try:
        content = await article_tpl.render_async(article=article)
        async with get_new_page(viewport={"width": 500, "height": 100}) as page:
            await page.set_content(content)
            img = await page.screenshot(full_page=True)
        return img
    except Exception as e:
        logger.warning(f"Error in create_image: {e}")
        return None
