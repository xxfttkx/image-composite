import io
import random
import requests
from PIL import Image
import numpy as np

def force_hard_alpha(img: Image.Image) -> Image.Image:
    """
    将所有 alpha 不等于 255 的像素设为完全透明，去除羽化边缘。
    """
    img = img.convert("RGBA")
    data = np.array(img)
    alpha = data[:, :, 3]

    # 找出 alpha 不为 255 的位置
    non_hard_alpha_mask = alpha != 255

    # 将这些像素设置为透明
    data[non_hard_alpha_mask] = [0, 0, 0, 0]

    return Image.fromarray(data, "RGBA")


def main():
    bodyArray = [1, 3, 4, 5, 7, 9]
    body_id = random.choice(bodyArray)
    if body_id == 9:
        CDN_BASE = "https://cdn.jsdelivr.net/gh/xxfttkx/image-hosting/aisa"
        body_url = f"{CDN_BASE}/{BODY_PATH}"
        body = Image.open(io.BytesIO(requests.get(body_url).content)).convert("RGBA")
        body.save("composite_aisa.png")
        return
    
    body_suffix = random.choice(['a', 'c'])
    BODY_PATH = f"ft藍咲_{body_id}{body_suffix}.png"

    # 根据权重选择 a1 或 a2
    face_type = random.choices(['a1', 'a2'], weights=[37, 19])[0]

    # 选择对应范围的 face_id
    face_id = random.randint(1, 37 if face_type == 'a1' else 19)

    FACE_PATH = f"ft04_{face_type}_{face_id}.png"

    # 打印输出（调试用）
    print("BODY_PATH:", BODY_PATH)
    print("FACE_PATH:", FACE_PATH)

    CDN_BASE = "https://cdn.jsdelivr.net/gh/xxfttkx/image-hosting/aisa"
    body_url = f"{CDN_BASE}/{BODY_PATH}"
    face_url = f"{CDN_BASE}/{FACE_PATH}"
    # 下载图片并打开
    body = Image.open(io.BytesIO(requests.get(body_url).content)).convert("RGBA")
    face = Image.open(io.BytesIO(requests.get(face_url).content)).convert("RGBA")
    # body_path = f"output_pngs_2/{BODY_PATH}"
    # face_path = f"output_pngs_2/{FACE_PATH}"
    # body = Image.open(body_path).convert("RGBA")
    # face = Image.open(face_path).convert("RGBA")
    face = force_hard_alpha(face)
    # 获取尺寸
    body_w, body_h = body.size
    face_w, face_h = face.size

    print("Body size:", body_w, body_h)
    print("Face size:", face_w, face_h)
    # 居中对齐（X 方向）
    x = int((body_w - face_w) / 2)-50

    # 手动微调贴图的 Y 位置
    y = 900
    tmp = Image.new("RGBA", body.size, (0, 0, 0, 0))
    tmp.paste(face, (x, y), mask=face)

    result = Image.alpha_composite(body, tmp)
    # tmp = Image.new("RGBA", body.size, (0, 0, 0, 0))
    # tmp.paste(face)
    # result = Image.alpha_composite(body,tmp)
    # result.show()
    # 保存结果
    result.save("composite_aisa.png")
    print("✅ 合成完成：composite_aisa.png")

if __name__ == "__main__":
    main()