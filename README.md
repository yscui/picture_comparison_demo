## Requirements

- Python 3.6+
- Android 4.4+

## Installation

    pip install uiautomator2
	pip install opencv-python

## 用法
将新闻的cmsid写入一个文本，每行一个，先通过脚本 run_automator.py 生成截图。
在测试环境运行时，设置变量:

	resultLR = 'l'

代表在左侧展示，在线上环境运行时，设置变量:

	resultLR = 'r'

代表在右侧展示。

两组截图生成完毕后再通过脚本 create_html.py 生成对比页面。

## 已知问题

- 客户端打开一个曾经打开过的页面会直接跳转到上次阅读的位置，导致无法截全，需要每次运行前重装客户端。
- 有动图或视频的页面可能无法正确拼接。
- 部分页面底部有展开按钮，目前无法正确点击展开。
