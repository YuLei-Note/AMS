from django.shortcuts import render
from django.shortcuts import redirect
# Create your views here.
from . import models
from . import forms
import datetime
import hashlib
from django.conf import settings


# 加密函数
def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


# 生成确认码
def make_confirm_string(user):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user)
    return code


# 邮件发送模块
def send_mail(email, code):
    from django.core.mail import EmailMultiAlternatives
    subject = '来自xxx的注册确认邮件'
    text_content = '正文部分'
    html_content = '''
    <p>感谢注册<a href='http://{}/confirm/?code={}' target=blank>点击完成注册</a></p>
    <p>此链接有效期为{}天！</p>
    '''.format('192.168.129.79:8000', code, settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


# # 主页逻辑模块
# def index(request):
#     # 未登录限制访问主页
#     if not request.session.get('is_login', None):
#         return redirect('/login/')
#     return render(request, 'assets/index.html')
#     # return render(request, 'login/index.html')


# 登陆模块
def login(request):
    # 不允许重复登陆
    if request.session.get('is_login', None):
        return redirect('/assets/index/')

    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = '检查填写内容！'
        # 表单自带的is_valid方法完成数据验证
        if login_form.is_valid():
            # 从表单的cleaned_data字典中获取表单的具体值
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user = models.User.objects.get(name=username)
            except:
                message = '用户不存在！'
                return render(request, 'login/login.html', locals())
            '''
            locals()函数是python的内置方法，它会返回当前所有的本地变量字典，
            在此处就相当于把{'message': message, 'login_form':login_form}
            作为render()的参数
            '''
            if not user.has_confirmed:
                message = '该用户还未经过确认！'
                return render(request, 'login/login.html', locals())

            if user.password == password:
                if user.is_superuser:
                    # 往session字典中写入用户状态和数据
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    request.session['u_team'] = user.get_u_team_display()
                    request.session['email'] = user.email
                    request.session['is_superuser'] = user.is_superuser
                    return redirect('/assets/index/')
                else:
                    # 往session字典中写入用户状态和数据
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    request.session['u_team'] = user.get_u_team_display()
                    request.session['email'] = user.email
                    request.session['is_superuser'] = user.is_superuser
                    return redirect('/assets/userpage/')
            else:
                message = '密码不正确！'
                return render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())
    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())


# 注册模块
def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            # sex = register_form.cleaned_data.get('sex')
            u_team = register_form.cleaned_data.get('u_team')

            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'login/register.html', locals())

                new_user = models.User()
                new_user.name = username
                new_user.password = password1
                new_user.email = email
                # new_user.sex = sex
                new_user.u_team = u_team
                new_user.save()

                code = make_confirm_string(new_user)
                send_mail(email, code)
                message = '请查收邮件进行注册确认！'

                return redirect('/login/')
        else:
            return render(request, 'login/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())


# 注销模块
def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    # 删除当前的会话数据和会话cookie
    request.session.flush()
    '''
    或者使用如下的删除方法：
    del request.session['is_login']
    del request.session['user_id']
    del request.session['user_name']
    '''
    return redirect('/login/')


# 用户注册确认
def user_confirm(request):
    # 从请求的地址中获取确认码
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求！'
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    # 注册码过期
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '邮箱已经过期！请重新注册！'
        return render(request, 'login/confirm.html', locals())
    # 未过期
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'login/confirm.html', locals())
