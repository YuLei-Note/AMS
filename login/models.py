from django.db import models


# Create your models here.


class User(models.Model):
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
    name = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    # sex = models.CharField(max_length=32, choices=gender, default='男')
    u_team = models.CharField(max_length=32, choices=team, default='Company')
    c_time = models.DateTimeField(auto_now_add=True)
    # 确认状态，默认是False
    has_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.name, self.get_u_team_display()

    class Meta:
        ordering = ['-c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'


class ConfirmString(models.Model):
    '''
    保存了用户和注册码之间的关系，一对一的形式；
    code：哈希后的注册码
    user：关联的一对一用户
    c_time：注册的提交时间
    '''
    code = models.CharField(max_length=256)
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name + ': ' + self.code

    class Meta:
        ordering = ['-c_time']
        verbose_name = '确认码'
        verbose_name_plural = '确认码'
