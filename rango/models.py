from django.db import models
from django.contrib import admin
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(blank=True)  # 别名,允许空值

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)  # 把空白字符替换为连字符,slugify()生成的别名是小写
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'  # 对象的复数名称,如果没有给定，Django 将使用 verbose_name + "s"

    def __str__(self):
        return self.name


class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    # @admin.display(
    #     boolean=True,
    #     ordering='category',
    #     description='Published recently?',
    # )
    def __str__(self):
        return self.title


# class Artist(models.Model):
#     name = models.CharField(max_length=10)
#
#
# class Album(models.Model):
#     artist = models.ForeignKey(Artist, on_delete=models.CASCADE)  # CASCADE表示级联，即删除的话所有包括此类的都删除
#
#
# class Song(models.Model):
#     artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
#     album = models.ForeignKey(Album, on_delete=models.RESTRICT)   # RESTRICT表示限制，如果其他类包括此类，那么删除此类会报错RestrictedError:


# artist_one = Artist.objects.create(name='artist one')
# artist_two = Artist.objects.create(name='artist two')
# album_one = Album.objects.create(artist=artist_one)
# album_two = Album.objects.create(artist=artist_two)
# song_one = Song.objects.create(artist=artist_one, album=album_one)
# song_two = Song.objects.create(artist=artist_one, album=album_two)
# album_one.delete()
# # Raises RestrictedError.
# artist_two.delete()
# # Raises RestrictedError.
# artist_one.delete()


class UserProfile(models.Model):
    # 建立与User模型之间的关系   这里的CASCADE是级联删除的意思，当主键删除时，从键跟着删除！
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # 想增加的属性
    website = models.URLField(blank=True)   # 该值可以为空
    # 头像存储的位置为E:\source code\Django\tango_with_django_project/media/profile_images/
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # 覆盖__str__()方法，返回有意义的字符串
    def __str__(self):
        return self.user.username


