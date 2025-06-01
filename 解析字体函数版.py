import ddddocr
from fontTools.ttLib import TTFont
from PIL import Image,ImageFont,ImageDraw


def parser_font(fontfile):
    ocr = ddddocr.DdddOcr(show_ad=False)
    # 修正：使用传入的fontfile参数而非字符串'fontfile'
    font = TTFont(fontfile)
    maps = font.getBestCmap()
    key_maps = {}

    for k, v in maps.items():
        name = chr(k)
        img = Image.new('RGB', (200, 200), color='red')
        draw = ImageDraw.Draw(img)
        # 修正：同样使用fontfile参数
        draw.text(
            xy=(50, 50),
            text=name,
            font=ImageFont.truetype(fontfile, size=100)
        )
        value = ocr.classification(img)
        key_maps[name] = value

    return key_maps

res = parser_font('sxs.woff')
print(res)

