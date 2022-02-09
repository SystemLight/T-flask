from random import choices

from PIL import Image
from captcha.image import ImageCaptcha


def gen_captcha(content='2345689abcdefghijklmnpqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ'):
    image = ImageCaptcha()  # 获取字符串
    captcha_text = "".join(choices(content, k=4)).lower()  # 生成图像
    captcha_image = Image.open(image.generate(captcha_text))
    return captcha_text, captcha_image
