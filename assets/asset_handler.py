from . import models
import json


def log(log_type, msg=None, asset=None, new_asset=None, request=None):
    '''
    日志模块
    :param log_type:
    :param msg:
    :param asset:
    :param new_asset:
    :param request:
    :return:
    '''
    pass


class ApproveAsset:
    '''
    审批资产并上线
    '''

    def __init__(self, request, asset_id):
        self.request = request
        self.new_asset = models.NewAssetApprovalZone.objects.get(id=asset_id)
        self.data = json.loads(self.new_asset.data)

    def asset_upline(self):
        '''其他类型的资产扩展接口'''
        print(self.new_asset.asset_type)
        func = getattr(self, '_{}_upline'.format(self.new_asset.asset_type))
        ret = func()
        return ret

    def _server_upline(self):
        pass

    def _computer_upline(self):
        asset = self._create_asset()
        self._create_cpu(asset)
        self._create_disk(asset)
        self._create_nic(asset)
        self._create_ram(asset)
        self._delete_original_asset()
        # try:
        #     self._create_cpu(asset)
        #     self._create_disk(asset)
        #     self._create_nic(asset)
        #     self._create_ram(asset)
        #     self._delete_original_asset()
        # except Exception as e:
        #     asset.delete()
        #     log('approve_failed', msg=e, new_asset=self.new_asset, request=self.request)
        #     print(e)
        #     return False
        # else:
        #     log('upline', asset=asset, request=self.request)
        #     print('新办公电脑上线！')
        #     return True

    def _create_asset(self):
        '''
        创建资产并上线
        :return:
        '''
        # request.user 获取当前管理员的信息，作为审批人添加到资产总表中
        asset = models.Asset.objects.create(asset_type=self.new_asset.asset_type,
                                            name='{}:{}'.format(self.new_asset.asset_type, self.new_asset.hostname),
                                            hostname=self.new_asset.hostname,
                                            user=self.new_asset.user,
                                            team=self.new_asset.team,
                                            approved_by=self.request.user,
                                            )
        return asset

    def _create_networkdevice(self):
        '''
        创建网络设备数据
        :return:
        '''
        pass

    def _create_server(self):
        '''
        创建服务器数据
        :return:
        '''
        pass

    def _create_storage(self):
        '''
        存储设备数据
        :return:
        '''
        pass

    def _create_computer(self, asset):
        '''
        办公电脑数据
        :return:
        '''
        # 缺少sub_asset_type参数
        models.Computer.objects.create(asset=asset,
                                       hostname=self.new_asset.hostname,
                                       os=self.new_asset.os,
                                       )
        pass

    def _create_cpu(self, asset):
        '''
        CPU数据
        :return:
        '''
        # cpu_data = self.data.get('cpu')
        # print('\n')
        # print(cpu_data)
        # print('\n')
        cpu = models.CPU.objects.create(asset=asset)
        cpu.cpu_model = self.data.get('cpu_model')
        cpu.cpu_core_count = self.data.get('cpu_core_count')
        cpu.cpu_count = self.data.get('cpu_count')
        cpu.save()

    def _create_ram(self, asset):
        '''
        内存数据
        :return:
        '''
        ram = models.RAM.objects.create(asset=asset)
        ram.model = self.new_asset.model
        ram.capacity = self.new_asset.ram_size
        ram.save()

    def _create_nic(self, asset):
        '''
        网卡数据
        :return:
        '''
        nic_list = self.data.get('nic')
        for nic_dict in nic_list:
            nic = models.NIC.objects.create(asset=asset)
            nic.model = nic_dict['model']
            nic.name = nic_dict['name']
            nic.ip_address = nic_dict['ip_address']
            nic.mac = nic_dict['mac']
            nic.save()

    def _create_disk(self, asset):
        '''
        硬盘数据
        :return:
        '''
        disk_data = self.data.get('disk_driver')
        if disk_data:
            for dis in disk_data:
                disk = models.Disk.objects.create(asset=asset)
                disk.interface_type = dis['interface_type']
                disk.capacity = dis['capacity']
                disk.save()
        else:
            return

    def _delete_original_asset(self):
        '''
        从待审批区删除已经成功上线的资产
        :return:
        '''
        self.new_asset.delete()
