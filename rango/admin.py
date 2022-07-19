from django.contrib import admin
from rango.models import Category, Page
from rango.models import UserProfile


# Register your models here.
class PageInline(admin.TabularInline):  # StackedInline
    model = Page
    extra = 1   # 只有一个额外的新的


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  # 在管理界面输入分类名称时自动填写别名
    fieldsets = [
        (None,               {'fields': ['name', 'slug']}),
        ('Date information', {'fields': ['views', 'likes'], 'classes': ['collapse']}),  # 设为默认隐藏
    ]
    inlines = [PageInline]  # page页面可在Category更改


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)
