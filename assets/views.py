from django.shortcuts import render
from django.shortcuts import HttpResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import json
from assets import models


class NewAsset:
    def __init__(self, request, data):
        self.request = request
        self.data = data

    def add_to_new_assets_zone(self):
        '''
        新资产加入待审批区模块
        将发送过来的数据打包成defauls字典，查询NewAssetApprovalZone中是否存在hostname相同的数据
        如果有，则修改defaults字典中的更新数据，
        如果没有，则新添加一条数据
        :return:
        '''
        defaults = {
            'data': json.dumps(self.data),
            'asset_type': self.data.get('asset_type'),
            'model': self.data.get('model'),
            'ram_size': self.data.get('sum_capacity'),
            'cpu_model': self.data.get('cpu_model'),
            'os': self.data.get('os_type'),
        }
        models.NewAssetApprovalZone.objects.update_or_create(hostname=self.data['hostname'], defaults=defaults)

        return '资产已经更新或者加入了资产待审批区！'


# 客户端数据收集模块
@csrf_exempt
def report(request):
    '''
    客户端脚本模拟浏览器向本服务端发送数据，请求中需要携带Django需要的CSRF安全令牌，否则会拒绝请求
    :param request:
    :return:
    '''
    if request.method == 'POST':
        data = json.loads(request.POST.get('asset_data'))
        '''
        此处需要对data数据进行检查
        '''
        if not data:
            return HttpResponse('没有数据！')
        if not issubclass(dict, type(data)):
            return HttpResponse('Wrong data type!')
        hostname = data.get('hostname', None)
        if hostname:
            # 进入审批流程，首先判断在原数据库中是否存在该条数据
            asset_obj = models.Asset.objects.filter(hostname=hostname)
            # 存在相同hostname的资产
            if asset_obj:
                # 进入已上线资产数据更新流程，写入日志
                pass
                return HttpResponse('资产数据已经更新!')
            else:
                # 进入新资产待审批区，更新或者创建数据
                response_to_client = NewAsset(request, data).add_to_new_assets_zone()
                return HttpResponse(response_to_client)
        else:
            return HttpResponse('没有资产hostname，请检查数据！')
    return HttpResponse('成功接收数据！')
