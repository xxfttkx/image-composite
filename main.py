import requests
from PIL import Image
from io import BytesIO
import os
import composite_kokoron
import composite_aisa

bg_url = os.getenv("BG_URL")

def paste_foreground(background, foreground, scale=1.0, offset=(0, 0)):
    """
    将前景图缩放后，按居中+偏移的位置合成到背景图上。

    :param background: PIL.Image 背景图（RGBA模式）
    :param foreground: PIL.Image 前景图（RGBA模式）
    :param scale: float 缩放比例，如0.5表示缩小到一半
    :param offset: tuple (x, y) 偏移量，基于居中位置的偏移
    """
    # 缩放前景图
    new_size = (int(foreground.width * scale), int(foreground.height * scale))
    fg_resized = foreground.resize(new_size, Image.LANCZOS)

    # 计算贴图位置（居中+偏移）
    x = (background.width - fg_resized.width) // 2 + offset[0]
    y = (background.height - fg_resized.height) // 2 + offset[1]

    # 贴图
    background.paste(fg_resized, (x, y), fg_resized)

def main():
    # 步骤 1: 下载背景图
    bg_url = os.getenv("BG_URL")
    response = requests.get(bg_url)
    background = Image.open(BytesIO(response.content)).convert("RGBA")

    # 步骤 2: 加载人物图像（当前目录下的 composite_aisa.png）
    foreground_0 = Image.open('composite_kokoron.png').convert("RGBA")
    foreground_1 = Image.open('composite_aisa.png').convert("RGBA")

    paste_foreground(background, foreground_0, scale=0.4, offset=(-300, background.height//4+200))
    paste_foreground(background, foreground_1, scale=0.5, offset=(300, background.height//4))


    # 步骤 5: 保存或显示结果
    background.save("result.png")
    background.show()

if __name__ == "__main__":
    composite_kokoron.main()
    composite_aisa.main()
    main()