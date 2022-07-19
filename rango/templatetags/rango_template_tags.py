# coding:utf-8
# @Time:2022/6/14 16:12
# @Author:LHT
# @File:rango_template_tags
# @GitHub:https://github.com/SHICUO
# @Contact:lin1042528352@163.com
# @Software:PyCharm

from django import template
from rango.models import Category

register = template.Library()  # 一个用于注册模板标签和过滤器的类。


@register.inclusion_tag('rango/cats.html')
def get_category_list(cat=None):
    return {'cats': Category.objects.all(), 'act_cat': cat}
