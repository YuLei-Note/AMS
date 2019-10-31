# 表单类
from django import forms
from captcha.fields import CaptchaField


class UserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username', 'autofocus': ''}))
    password = forms.CharField(label='密码', max_length=256, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))
    captcha = CaptchaField(label='验证码')


class RegisterForm(forms.Form):
    # gender = (
    #     ('male', '男'),
    #     ('female', '女'),
    # )
    team = (
        ('0', 'Beacon'),
        ('1', 'Company'),
        ('2', 'Compass'),
        ('3', 'Eagles'),
        ('4', 'IT'),
        ('5', 'Nova'),
        ('6', 'OP'),
        ('7', 'Rainbow'),
        ('8', 'Sales&Market'),
        ('9', 'STS'),
        ('10', 'UI'),
        ('11', 'Vanguard'),
    )
    username = forms.CharField(label='用户名', max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='密码', max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='确认密码', max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='邮箱', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    u_team = forms.ChoiceField(label='所属组', choices=team)
    captcha = CaptchaField(label='验证码')
