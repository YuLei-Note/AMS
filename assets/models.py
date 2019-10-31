from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# 资产总表
class Asset(models.Model):
    asset_type_choice = (
        ('networkdevice', '网络设备'),
        ('server', '服务器'),
        ('storage', '存储设备'),
        ('computer', '办公电脑'),
        ('ithardware', 'IT配件'),
        ('software', '软件资产')
    )
    asset_status = (
        (0, '在用'),
        (1, '闲置'),
        (2, '损坏'),
        (3, '报废'),
    )
    hostname = models.CharField(max_length=32, unique=True, verbose_name='资产编号')
    asset_type = models.CharField(choices=asset_type_choice, max_length=64, default='server', verbose_name='资产类型')
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name='资产名称')
    status = models.SmallIntegerField(choices=asset_status, default=0, verbose_name='设备状态')
    # 临时字段，版本更新外键关联
    user = models.CharField(max_length=32, blank=True, null=True, verbose_name='使用人')
    team = models.CharField(max_length=32, blank=True, null=True, verbose_name='所在组')
    manage_user = models.ForeignKey(User, null=True, blank=True, verbose_name='资产管理员',
                                    related_name='admin', on_delete=models.SET_NULL)
    approved_by = models.ForeignKey(User, null=True, blank=True, verbose_name='批准人', related_name='approved_by',
                                    on_delete=models.SET_NULL)
    price = models.FloatField(null=True, blank=True, verbose_name='价格')
    memo = models.TextField(null=True, blank=True, verbose_name='备注')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='批准日期')
    m_time = models.DateTimeField(auto_now_add=True, verbose_name='更新日期')

    def __str__(self):
        return '%s %s' % (self.get_asset_type_display(), self.hostname)

    class Meta:
        verbose_name = '资产总表'
        verbose_name_plural = '资产总表'
        ordering = ['-c_time']


# 网络设备
class NetworkDevice(models.Model):
    sub_asset_type_choice = (
        (0, '防火墙'),
        (1, '路由器'),
        (2, '交换机'),
        (3, '行为管理设备')
    )
    # 一对一字段，asset被删除的时候，一并删除NetworkDevice
    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name='网络设备')
    model = models.CharField(max_length=128, default='未知型号', verbose_name='网络设备型号')

    def __str__(self):
        return self.asset.name, self.get_sub_asset_type_display()

    class Meta:
        verbose_name = '网络设备'
        verbose_name_plural = '网络设备'


# 服务器
class Server(models.Model):
    sub_asset_type_choice = (
        (0, 'PC服务器'),
        (1, '正式服务器'),
    )
    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name='服务器类型')
    host_on = models.ForeignKey('self', related_name='hosted_on_server', on_delete=models.CASCADE, blank=True,
                                null=True,
                                verbose_name='宿主机')
    model = models.CharField(max_length=128, null=True, blank=True, verbose_name='服务器型号')
    os_type = models.CharField('操作系统', max_length=64, blank=True, null=True)

    def __str__(self):
        return self.asset.name

    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = '服务器'


# 存储
class Storage(models.Model):
    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    model = models.CharField(max_length=128, default='未知型号', verbose_name='存储设备型号')
    storage_capacity = models.IntegerField(default=0, verbose_name='存储容量')

    def __str__(self):
        return self.asset.name, self.model

    class Meta:
        verbose_name = '存储设备'
        verbose_name_plural = '存储设备'


# 办公电脑
class Computer(models.Model):
    sub_asset_type_choice = (
        (0, '台式机'),
        (1, '笔记本'),
    )
    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    sub_asset_type = models.CharField(choices=sub_asset_type_choice, max_length=64, default='台式机', verbose_name='电脑类型')
    hostname = models.CharField(max_length=24, primary_key=True, verbose_name='设备IT编号')
    os = models.CharField(max_length=64, default='Windows', blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.get_sub_asset_type_display(), self.asset.name)

    class Meta:
        verbose_name = '电脑资产'
        verbose_name_plural = '电脑资产'


# CPU
class CPU(models.Model):
    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    cpu_model = models.CharField('CPU型号', max_length=128)
    cpu_count = models.PositiveSmallIntegerField('物理CPU个数', default=1)
    cpu_core_count = models.PositiveSmallIntegerField('CPU核数', default=1)

    def __str__(self):
        return self.asset.name + ': ' + self.cpu_model

    class Meta:
        verbose_name = 'CPU'
        verbose_name_plural = 'CPU'


# 内存
class RAM(models.Model):
    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    model = models.CharField('内存型号', max_length=128, blank=True, null=True)
    capacity = models.IntegerField('内存大小', blank=True, null=True)

    def __str__(self):
        return '{}:{}:{}'.format(self.asset.name, self.model, self.capacity)

    class Meta:
        verbose_name = 'RAM'
        verbose_name_plural = 'RAM'


# 硬盘
class Disk(models.Model):
    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    interface_type = models.CharField('硬盘类型', max_length=64, blank=True, null=True)
    capacity = models.FloatField('磁盘容量', blank=True, null=True)

    def __str__(self):
        return '{}:{}'.format(self.asset.name, self.capacity)

    class Meta:
        verbose_name = '硬盘'
        verbose_name_plural = '硬盘'


# 网卡
class NIC(models.Model):
    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    name = models.CharField('网卡名称', max_length=64, blank=True, null=True)
    model = models.CharField('网卡ID', max_length=128)
    mac = models.CharField('MAC地址', max_length=64)
    ip_address = models.GenericIPAddressField('IP地址', blank=True, null=True)

    def __str__(self):
        return '{}:{}:{}'.format(self.asset.name, self.model, self.mac)

    class Meta:
        verbose_name = '网卡'
        verbose_name_plural = '网卡'


# 日志模块
class EventLog(models.Model):
    """
    日志模块
    关联对象被删除的时候，需要保留日志
    on_delete=models.SET_NULL
    """
    name = models.CharField('事件名称', max_length=128)
    event_type_choice = (
        (0, '其他'),
        (1, '硬件变更'),
        (2, '新增配件'),
        (3, '设备下线'),
        (4, '设备上线'),
    )
    asset = models.ForeignKey('Asset', blank=True, null=True, on_delete=models.SET_NULL)
    new_asset = models.ForeignKey('NewAssetApprovalZone', blank=True, null=True, on_delete=models.SET_NULL)
    event_type = models.SmallIntegerField('事件类型', choices=event_type_choice, default=0)
    detail = models.TextField('事件详细')
    date = models.DateTimeField('事件时间', auto_now_add=True)
    user = models.ForeignKey(User, blank=True, null=True, verbose_name='事件执行人', on_delete=models.SET_NULL)
    memo = models.TextField('备注', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '事件记录'
        verbose_name_plural = '事件记录'


# 新上线资产待审批模块
class NewAssetApprovalZone(models.Model):
    asset_type_choice = (
        ('server', '服务器'),
        ('computer', '办公电脑'),
    )
    hostname = models.CharField('设备IT编号', max_length=32, unique=True)
    user = models.EmailField('使用人邮箱', null=True, blank=True)
    team = models.CharField('所在组', max_length=32, null=True, blank=True)
    asset_type = models.CharField(choices=asset_type_choice, default='办公电脑', max_length=64, blank=True, null=True,
                                  verbose_name='资产类型')
    sub_asset_type = models.CharField(max_length=32, default='台式机', blank=True, null=True, verbose_name='子类型')
    model = models.CharField(max_length=128, blank=True, null=True, verbose_name='型号')
    ram_size = models.PositiveIntegerField(blank=True, null=True, verbose_name='内存大小')
    cpu_model = models.CharField(max_length=128, blank=True, null=True, verbose_name='CPU型号')
    os = models.CharField('操作系统', max_length=64, blank=True, null=True)
    data = models.TextField('资产数据')
    c_time = models.DateTimeField('上传日期', auto_now_add=True)
    m_time = models.DateTimeField('数据更新日期', auto_now_add=True)
    approved = models.BooleanField('是否批准', default=False)

    def __str__(self):
        return self.hostname

    class Meta:
        verbose_name = '新上线待审批资产'
        verbose_name_plural = '新上线待审批资产'
