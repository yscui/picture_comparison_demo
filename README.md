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


## create_html.py

将两组照片上传到html中，后续可以肉眼直观查看两组图片的不同之处
