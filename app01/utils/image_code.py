import random

from PIL import Image, ImageFont, ImageDraw, ImageFilter


def check_code(width=120, height=30, char_length=5, font_file='Monaco.ttf', font_size=28):
    code = []
    img = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))

    draw = ImageDraw.Draw(img, mode="RGB")

    def rndChar():
        return chr(random.randint(65, 90))

    def rndColor():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # 生成随机5个字母
    font = ImageFont.truetype(font_file, font_size)
    for i in range(char_length):
        ch = rndChar()
        code.append(ch)
        h = random.randint(0, 4)
        draw.text([i * width / char_length, h], ch, font=font, fill=rndColor())

    # 写干扰点
    for i in range(100):
        draw.point([random.randint(0, 120), random.randint(0, 30)], fill=rndColor())

    # 写干扰线
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=rndColor())

    # 写干扰圆
    for i in range(40):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        draw.arc((x1, y1, x1 + 4, y1 + 4), 0, 90, fill=rndColor())

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)

    return img, ''.join(code)
