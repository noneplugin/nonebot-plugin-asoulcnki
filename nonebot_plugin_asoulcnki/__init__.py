from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event

from .data_source import check_text


__help__plugin_name__ = 'asoulcnki'
__des__ = '枝网查重'
__cmd__ = '''
查重 {text}
'''.strip()
__short_cmd__ = __cmd__
__example__ = '''
查重
然然，我今天发工资了，发了1300。你肯定觉得我会借14块钱，然后给你打个1314块的sc对不对？不是哦，我一块都不打给你，因为我要打给乃琳捏
'''.strip()
__usage__ = f'{__des__}\nUsage:\n{__cmd__}\nExample:\n{__example__}'


asoulcnki = on_command('asoulcnki', aliases={'枝网查重', '查重'})


@asoulcnki.handle()
async def _(bot: Bot, event: Event, state: T_State):
    text = event.get_plaintext().strip()
    if not text:
        await asoulcnki.finish()

    if len(text) >= 1000:
        await asoulcnki.finish('文本过长，长度须在10-1000之间')
    elif len(text) <= 10:
        await asoulcnki.finish('文本过短，长度须在10-1000之间')

    msg = await check_text(text)
    if msg:
        await asoulcnki.finish(msg)
    else:
        await asoulcnki.finish('出错了，请稍后再试')
