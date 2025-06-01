from PIL import Image, ImageDraw, ImageFont
from ddddocr import DdddOcr
from fontTools.ttLib import TTFont


class ParserFontFile:
    """解析字体文件中的映射关系"""
    ocr = DdddOcr(show_ad=False)

    def __init__(self, filename):
        fonts = TTFont(filename)
        # 获取字符和字形的映射关系
        maps = fonts.getBestCmap()
        # 识别字符和字形的映射内容]
        self.font_maps = {}
        for k in maps:
            self.font_maps[chr(k)] = self.str_to_value(chr(k), filename)

    def str_to_value(self, unicode, font_file):
        """识别字符在字体文件中的字形内容"""
        # 创建一张图片(色彩模式为RGB，大小为200*200像素，颜色为红色)
        img = Image.new('RGB', (200, 200), 'red')
        # 创建一个画笔
        draw = ImageDraw.Draw(img)
        # 加载字体文件
        font = ImageFont.truetype(font_file, 100)
        # 使用画笔在文件中写入内容
        draw.text((50, 50), unicode, font=font)
        # 识别生成的图片中的内容
        value = self.ocr.classification(img)
        return value


if __name__ == '__main__':
    maps = ParserFontFile('58.ttf') # 只需修改括号内的文件名即可将对应的映射关系转化出来
    print(maps.font_maps)
