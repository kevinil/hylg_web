# -*- coding:utf-8 -*-
import os
import sys
import django


# 可视化依赖库
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import PIL .Image as image
import numpy as np
import jieba
from imageio import imread

# 遮照图片
back_color = imread('ditu.png')

# 词云
wc = WordCloud(mask=back_color,
               background_color="white",
               max_words=1000,
               max_font_size=100,
               collocations=False,
               font_path='msyhbd.ttf',
               width=500,
               height=365,
               random_state=42)


# 路径
pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, pathname)
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
# 连接django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hylg_web.settings")
django.setup()
# 导入models
from hy_case.models import CaseData, Customer

def wcGenerate(text):
    wc.generate(text)
    image_colors = ImageColorGenerator(back_color)
    plt.imshow(wc)
    plt.axis('off')
    plt.figure()
    plt.imshow(wc.recolor(color_func=image_colors))
    plt.axis('off')
    wc.to_file('/Users/kevin/WorkSpace/hylg_web/hylg_vue/src/assets/huaying.png')

def caseWcGenerate():
    cloud_array = []
    for o in CaseData.objects.all():
        if (o.case_person[-1] == "/r"):
            print("get")
        cloud_array.append(o.case_person)
    print(cloud_array)
    cloud_string = " ".join(cloud_array)
    wc.generate(cloud_string)
    image_colors = ImageColorGenerator(back_color)
    plt.imshow(wc)
    plt.axis('off')
    plt.figure()
    plt.imshow(wc.recolor(color_func=image_colors))
    plt.axis('off')
    wc.to_file('/Users/kevin/WorkSpace/hylg_web/hylg_vue/src/assets/caseCloud.png')


