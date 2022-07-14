import os
import cv2
import time
import uiautomator2 as u2

resultLR = 'l'
inputFile = r"D:\Projects\news-screenshot\input.txt"
outputDir = r"D:\Projects\news-screenshot"

if __name__ == '__main__':
    imgDir = os.path.join(outputDir, "img")
    if not os.path.exists(imgDir):
        os.makedirs(imgDir)
    with open(inputFile) as f:
        lines = f.readlines()

    d = u2.connect_usb()
    d.screen_on()

    for index, line in enumerate(lines):
        cid = line.strip()

        d.app_stop("com.tencent.news")
        time.sleep(1)
        d.shell("am start "
                + "-c android.intent.category.BROWSABLE "
                + "-a android.intent.action.VIEW "
                + "-d https://view.inews.qq.com/a/" + cid + " "
                + "com.tencent.news")
        time.sleep(10)

        # 内容区域，需要避开下边控件的阴影区域，10像素足够了
        cContentStart = d(resourceId="com.tencent.news:id/content_center")
        if cContentStart.exists():
            nContentStart = cContentStart.info['bounds']['bottom']
        else:
            continue
        cContentEnd = d(resourceId="com.tencent.news:id/action_bar_zan")
        if cContentEnd.exists():
            nContentEnd = cContentEnd.info['bounds']['top'] - 10
        else:
            continue
        nContentHeight = nContentEnd - nContentStart
        nTailHeight = int(nContentHeight * 0.4)

        # 理论上配准后的位置，如果差别太大表示配准失败了
        nCutStart = nContentStart + int(nContentHeight * 0.6)

        # 每次滑动内容高度的40%，因为滑动可能存在误差，导致多滑，需要保证滑动距离不能超过内容的一半
        nScreenHeight = d.info['displayHeight']
        nSwipeStart = nScreenHeight / 2 + nContentHeight * 0.2
        nSwipeEnd = nScreenHeight / 2 - nContentHeight * 0.2

        dst = None
        lastTail = None
        while True:

            # 先处理有广告和展开全文的情况
            cCollapse = d(resourceId="com.tencent.news:id/collapse_mask_icon")
            if cCollapse.exists():
                cCollapse.click()
                time.sleep(5)

            img = d.screenshot(format='opencv')
            cEndLine = d(resourceId="com.tencent.news:id/interaction_root")

            # 截屏的终止线
            nEndPos = nContentEnd
            if cEndLine.exists():
                nEndPos = cEndLine.info['bounds']['top']

            # 首次截屏
            if dst is None:
                dst = img[nContentStart: nEndPos, :]

            # 非首次截屏需要配准拼接
            else:
                res = cv2.matchTemplate(img, lastTail, cv2.TM_CCOEFF)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                nCutStartMT = max_loc[1] + nTailHeight
                if abs(nCutStartMT - nCutStart) > nContentHeight * 0.1:
                    nCutStartMT = nCutStart
                cut = img[nCutStartMT: nEndPos]
                dst = cv2.vconcat([dst, cut])

            if cEndLine.exists():
                break

            # 保存上次截屏的40%尾部区域用于配准
            lastTail = img[nEndPos - nTailHeight: nEndPos, :].copy()

            # 滑动出新的40%内容区域
            d.swipe(100, nSwipeStart, 100, nSwipeEnd, 0.3)
            time.sleep(0.1)

        imageFileName = str(index) + '-' + resultLR + '.png'
        cv2.imwrite(os.path.join(imgDir, imageFileName), dst)
