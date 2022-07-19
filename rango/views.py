from django.shortcuts import render
from django.shortcuts import redirect, reverse
from rango.models import Category, Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime


def index(request):
    # 测试是否支持cookie
    request.session.set_test_cookie()

    """
    # 构建一个字典，作为上下文传给模板引擎
    # 注意，boldmessage 键对应于模板中的{{boldmessage}}
    context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}

    # 返回一个渲染后的响应发给客户端
    # 为了方便，我们使用的是render函数的简短形式
    # 注意，第二个参数是我们想使用的模板
    return render(request, 'rango/index.html', context_dict)
    """
    # 查询数据库，获取目前存储的所有分类
    # 按点赞次数倒序排列分类
    # 获取前5个分类（如果分类数少于5个，那就获取全部）
    # 把分类列表放入 context_dict 字典
    # 稍后传给模板引擎
    category_list = Category.objects.order_by('-likes')[:5]  # '-'表示倒序
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}

    # 调用处理 cookie 的辅助函数
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    # print(request.COOKIES.get('visits'))

    # 提取获取 response 对象，以便添加 cookie
    response = render(request, 'rango/index.html', context_dict)

    return response


def about(request):
    # 测试是否支持cookie
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()

    # return HttpResponse("Rango says here is the about page. <br/> <a href='/rango/'>Index</a>.")

    # 使用render
    # 打印请求方法，是get还是post
    print(request.method)
    # 打印用户名，如未登录，打印“AnonymousUser”
    print(request.user)
    return render(request, 'rango/about.html', {})


def show_category(request, category_name_slug):  # 显示分类信息页面
    # 创建上下文字典，稍后传给模板渲染引擎
    context_dict = {}

    try:
        # 通过传入的分类别名找到对应的分类
        # 如果找不到，.get()方法抛出DoesNotExist异常
        # 因此.get()方法返回一个模型实例或抛出异常
        category = Category.objects.get(slug=category_name_slug)

        # 检索关联的所有网页
        # 注意，filter()返回一个网页对象列表或空列表
        pages = Page.objects.filter(category=category)

        # 把得到的列表赋值给模板上下文中名为pages的键
        context_dict['pages'] = pages
        # 也把从数据库中获取的category对象添加到上下文字典中
        # 我们将在模板中通过这个变量确认分类是否存在
        context_dict['category'] = category
    except Category.DoesNotExist:
        # 没找到指定的分类时执行这里
        # 模板会显示消息，指明分类不存在
        context_dict['category'] = None
        context_dict['pages'] = None

    # 渲染响应，返回给客户端
    return render(request, 'rango/category.html', context_dict)


@login_required
def add_category(request):
    form = CategoryForm()

    # 判断是否HTTP POST请求
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # 判断表单数据是否有效
        if form.is_valid():
            # 把新分类存入数据库
            cat = form.save(commit=True)
            print(cat, cat.slug)    # 打印消息
            # 保存新分类后可以显示一个确认消息
            # 返回首页
            return index(request)
        else:
            # 表单数据有误，直接打印出来
            print(form.errors)

    # 渲染表单，并显示可能出现的错误消息
    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    # if category is None:
    #     return redirect()

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)


# def register(request):
#     # 一个布尔值，告诉模板注册是否成功
#     # 一开始设为False，注册成功后改为True
#     registered = False
#
#     # 如果是HTTP POST请求，处理表单数据
#     if request.method == 'POST':
#         # 获取表单数据
#         user_form = UserForm(data=request.POST)
#         print(user_form, '-------')
#         profile_form = UserProfileForm(data=request.POST)
#         print(profile_form)
#
#         # 如果两个表单中的数据是有效的
#         if user_form.is_valid() and profile_form.is_valid():
#             # 把UserForm中的数据存入数据库
#             user = user_form.save()
#
#             # 使用set_password方法计算密码哈希值，然后更新user对象
#             user.set_password(user.password)
#             user.save()
#
#             # 现在处理UserProfile实例
#             # 因为要自行处理user属性，所以设定commit=False
#             # 延迟保存模型，以防出现完整性问题
#             profile = profile_form.save(commit=False)
#             profile.user = user
#
#             # 如果用户提供了图像，从表单数据库中提取出来，赋给Userprofile模型
#             if 'picture' in request.FILES:
#                 profile.picture = request.FILES['picture']
#
#             # 保存Userprofile模型实例
#             profile.save()
#
#             # 更新变量的值，告诉模板成功注册
#             registered = True
#
#         else:
#             # 表单数据无效？打印问题
#             print(user_form.errors, profile_form.errors)
#
#     else:
#         # 不是HTTP POST请求，渲染两个ModelForm实例
#         # 表单为空，待用户填写
#         user_form = UserForm()
#         profile_form = UserProfileForm()
#
#     # 渲染模板
#     return render(request, 'rango/register.html',
#                   {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


# def user_login(request):
#     # 如果是HTTP POST请求，尝试提取相关信息
#     if request.method == 'POST':
#         # 获取用户在登录表单中输入的用户名和密码
#         # 我们使用的是request.POST.get('<variable>')
#         # 而不是request.POST['<variable>']
#         # 这是因为对应的值不存在时，前者返回None，后者返回抛出KeyError异常
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         # 使用Django提供的函数检查username/password是否有效，如有效返回一个User对象
#         user = authenticate(username=username, password=password)
#
#         # 如果得到了User对象，说明用户输入的凭据是对的
#         # 如果是None，则说明没找到与凭据匹配的用户
#         if user:
#             # 账户激活了吗
#             if user.is_active:
#                 # 登录有效且已激活的账户，然后重定向到首页
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#             else:
#                 # 账户未激活，禁止登录
#                 return HttpResponse("Your Rango account is disabled.")
#         # 提供的登录凭据有问题，不能登录
#         else:
#             print("Invalid login details:{0}, {1}".format(username, password))
#             return HttpResponse("Invalid login details supplied.用户名与密码不匹配！")
#
#     # 不是HTTP POST请求，显示登录表单，可能是get请求
#     else:
#         # 无内容传入
#         return render(request, 'rango/login.html', {})


# 检测是否登录
@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})


# 只有已登录的用户才能访问这个视图
# @login_required
# def user_logout(request):
#     # 可以确定用户已登录，因此直接退出
#     logout(request)
#     # 重定向回首页
#     return HttpResponseRedirect(reverse('index'))


# 统计访问次数。不是视图函数，是个辅助函数，因为不返回response对象
# def visitor_cookie_handler(request, response):
#     # 获取网站的访问次数
#     # 使用 COOKIES.get() 函数读取“visits”cookie
#     # 如果目标 cookie 存在，把值转换为整数，不存在则返回默认值1
#     visits = int(request.COOKIES.get('visits', '1'))
#
#     last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
#     last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
#
#     # 如果距上次访问已超过5s, 访问次数+1
#     if (datetime.now() - last_visit_time).seconds > 5:
#         visits = visits + 1
#         # 增加访问次数后更新“last_visit”cookie
#         response.set_cookie('last_visit', str(datetime.now()))
#     else:
#         # “last_visit”cookie 不变
#         response.set_cookie('last_visit', last_visit_cookie)
#
#     # 更新“visits”cookie, 第一次是创建
#     response.set_cookie('visits', visits)


# 辅助函数，获取cookie
# request.session.get 通过 session id 去获取cookie
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:   # 如果为空，默认值
        val = default_val
    return val


def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    # 如果距上次访问已超过5s, 访问次数+1
    if (datetime.now() - last_visit_time).seconds > 5:
        visits = visits + 1
        # 增加访问次数后更新“last_visit”cookie
        request.session['last_visit'] = str(datetime.now())
    else:
        # “last_visit”cookie 不变
        request.session['last_visit'] = last_visit_cookie

    # 更新“visits”cookie, 第一次是创建
    request.session['visits'] = visits


