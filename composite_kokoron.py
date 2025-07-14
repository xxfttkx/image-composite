import io
from PIL import Image
import random
import requests

def main():
    # 输入路径
    bodyArray = [1,10,11,12,13,15,17,18,19,2,20,21,23,3,4,5,7,9]
    faceArray = list(range(1, 31))  # [1, 2, 3, ..., 30]

    # 随机选择一个 body 和 face 数字
    body_id = random.choice(bodyArray)
    face_id = random.choice(faceArray)

    BODY_PATH = f"stb1_s0_1_{body_id}.png"
    FACE_PATH = f"st1_s0_1_{face_id}.png"

    CDN_BASE = "https://cdn.jsdelivr.net/gh/xxfttkx/image-hosting/kokoron"
    body_url = f"{CDN_BASE}/{BODY_PATH}"
    face_url = f"{CDN_BASE}/{FACE_PATH}"

    # 下载图片并打开
    body = Image.open(io.BytesIO(requests.get(body_url).content)).convert("RGBA")
    face = Image.open(io.BytesIO(requests.get(face_url).content)).convert("RGBA")

    tmp = Image.new("RGBA", body.size, (0, 0, 0, 0))
    tmp.paste(face)
    result = Image.alpha_composite(body,tmp)
    # result.show()
    # 保存结果
    result.save("composite_kokoron.png")
    print("✅ 合成完成：composite_kokoron.png")

if __name__ == "__main__":
    main()