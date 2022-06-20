from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import MessageEvent, Message

from .data_source import check_text, random_text


__plugin_meta__ = PluginMetadata(
    name="枝网查重",
    description="查询发病小作文重复率",
    usage="1、查重 xxx 或 回复内容“查重”\n2、小作文 [keyword]，随机小作文",
    extra={
        "unique_name": "asoulcnki",
        "example": "查重 我好想做嘉然小姐的狗啊",
        "author": "meetwq <meetwq@gmail.com>",
        "version": "0.2.1",
    },
)


asoulcnki = on_command("asoulcnki", aliases={"枝网查重", "查重"}, block=True, priority=13)


@asoulcnki.handle()
async def _(event: MessageEvent, msg: Message = CommandArg()):
    text = msg.extract_plain_text().strip()
    if not text:
        if event.reply:
            reply = event.reply.message.extract_plain_text().strip()
            if reply:
                text = reply

    if not text:
        await asoulcnki.finish()

    if len(text) >= 1000:
        await asoulcnki.finish("文本过长，长度须在10-1000之间")
    elif len(text) <= 10:
        await asoulcnki.finish("文本过短，长度须在10-1000之间")

    try:
        res = await check_text(text)
    except:
        await asoulcnki.finish("出错了，请稍后再试")
    await asoulcnki.finish(res)


article = on_command("小作文", aliases={"随机小作文", "发病小作文"}, block=True, priority=13)


@article.handle()
async def _(msg: Message = CommandArg()):
    keyword = msg.extract_plain_text().strip()

    try:
        res = await random_text(keyword)
    except:
        await article.finish("出错了，请稍后再试")
    await article.finish(res)
