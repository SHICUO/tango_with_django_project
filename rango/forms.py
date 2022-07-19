# coding:utf-8
# @Time:2022/5/5 18:45
# @Author:LHT
# @File:forms
# @GitHub:https://github.com/SHICUO
# @Contact:lin1042528352@163.com
# @Software:PyCharm

from django import forms
from rango.models import Page, Category, UserProfile
from django.contrib.auth.models import User


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # 嵌套的类，为表单提供额外信息
    class Meta:
        # 把这个ModelForm与一个模型连接起来
        model = Category
        fields = ('name', )


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        # 把这个ModelForm与一个模型连接起来
        model = Page

        # 隐藏外键字段category
        exclude = ('category', )
        # 也可以直接指定想显示的字段（不含category字段）
        # fields = ('title', 'url', 'views')

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        # 如果url字段不为空，且不以"https://"开头, 则在前面加上"https://"
        if url and not url.startswith(r'https://'):
            url = r'https://' + url
            cleaned_data['url'] = url

            return cleaned_data


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())    # 隐藏密码的输入

    class Meta:   # 作用：为所在的类提供额外的属性
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = 'website', 'picture'


