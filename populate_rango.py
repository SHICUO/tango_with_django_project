# coding:utf-8
# @Time:2022/4/29 19:45
# @Author:LHT
# @File:populate_rango
# @GitHub:https://github.com/SHICUO
# @Contact:lin1042528352@163.com
# @Software:PyCharm

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')
django.setup()

from rango.models import Category, Page


def populate():
    # 首先创建一些字典，列出想添加到各分类的网页
    # 然后创建一些嵌套字典，设置各分类
    # 这么做看起来不易理解，但是便于迭代，方便为模型添加数据
    python_pages = [
        {"title": "Official Python Tutorial",
         "url": "https://docs.python.org/3.8/tutorial/",
         "views": 32},
        {"title": "How to Think like a Computer Scientist",
         "url": "https://www.greenteapress.com/thinkpython/",
         "views": 16},
        {"title": "Learn Python in 10 Minutes",
         "url": "https://www.korokithakis.net/tutorials/python/",
         "views": 8},
    ]
    django_pages = [
        {"title": "Official Django Tutorial",
         "url": "https://docs.djangoproject.com/en/4.0/intro/tutorial01/",
         "views": 32},
        {"title": "Django Rocks",
         "url": "https://www.djangorocks.com/",
         "views": 16},
        {"title": "How to Tango with Django",
         "url": "https://www.tangowithdjango.com/",
         "views": 8},
    ]
    other_pages = [
        {"title": "Bottle",
         "url": "https://bottlepy.org/docs/dev/",
         "views": 32},
        {"title": "Baidu Search",
         "url": "https://www.baidu.com",
         "views": 16},
    ]

    cats = {
        "Python": {"pages": python_pages, "views": 128, "likes": 64},
        "Django": {"pages": django_pages, "views": 64, "likes": 32},
        "Other Frameworks": {"pages": other_pages, "views": 32, "likes": 16},
        "Pascal": {"pages": [], "views": 32, "likes": 16},
        "Perl": {"pages": [], "views": 32, "likes": 16},
        "Php": {"pages": [], "views": 32, "likes": 16},
        "Prolog": {"pages": [], "views": 32, "likes": 16},
        "Programming": {"pages": [], "views": 32, "likes": 16},
    }

    # 下述代码迭代cats字典，添加各分类，并把相关的网页添加到分类中
    # 迭代字典的正确方式参见：https://docs.quantifiedcode.com/python-anti-patterns/readability/
    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data["views"], cat_data["likes"])
        for p in cat_data["pages"]:
            add_page(c, p["title"], p["url"], p["views"])
    # 打印添加的分类
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))


def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    # 添加views和likes
    c.views = views
    c.likes = likes
    c.save()
    return c


def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p


if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()
