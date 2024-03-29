# nonebot-plugin-asoulcnki

NoneBot 枝网查重插件

利用 [枝网查重](https://asoulcnki.asia/) 查找最相似的小作文，为防止文字太长刷屏，将内容转换为图片形式发出

由于枝网项目组已停止活动，本插件已不可用。[关于枝网项目组暂时停止活动的公告](https://t.bilibili.com/658607344806002729)

### 使用方式

**以下命令需要加[命令前缀](https://v2.nonebot.dev/docs/api/config#Config-command_start) (默认为`/`)，可自行设置为空**

- 查重/枝网查重 + 要查重的小作文

- 回复需要查重的内容，回复“查重”

- 小作文/随机小作文


### 安装

- 使用 nb-cli

```
nb plugin install nonebot_plugin_asoulcnki
```

- 使用 pip

```
pip install nonebot_plugin_asoulcnki
```


### 示例

<div align="left">
  <img src="./examples/1.png" width="500" />
</div>


### 特别感谢

- [ASoulCnki/ASoulCnkiFrontEndV3](https://github.com/ASoulCnki/ASoulCnkiFrontEndV3) 参考了该项目的界面和查重代码

- [cscs181/QQ-GitHub-Bot](https://github.com/cscs181/QQ-GitHub-Bot) 参考了 playwright 的使用以及图片生成的方式

