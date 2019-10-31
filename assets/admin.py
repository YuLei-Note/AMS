from django.contrib import admin
from . import models
# Register your models here.
from . import asset_handler


class NewAssetAdmin(admin.ModelAdmin):
    list_display = [
        'hostname',
        'asset_type',
        'cpu_model',
        'ram_size',
        'c_time',
        'm_time',
    ]
    list_filter = ['asset_type', 'c_time']
    search_fields = ('hostname',)
    actions = ['approve_select_new_assets']

    def approve_select_new_assets(self, request, queryset):
        # 获得被打勾的对应的资产
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        success_upline_number = 0
        for asset_id in selected:
            # 批准资产上线模块
            obj = asset_handler.ApproveAsset(request, asset_id)
            ret = obj.asset_upline()
            if ret:
                success_upline_number += 1
        self.message_user(request, '成功批准{}条资产上线'.format(success_upline_number))

    approve_select_new_assets.short_description = '批准选择的资产'


class AssetAdmin(admin.ModelAdmin):
    list_display = [
        'asset_type',
        'hostname',
        'status',
        'user',
        'team',
        'approved_by',
        'm_time',
    ]


class EventAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'event_type',
        'date',
        'user',
    ]


admin.site.register(models.Asset, AssetAdmin)
admin.site.register(models.NetworkDevice)
admin.site.register(models.Server)
admin.site.register(models.Storage)
admin.site.register(models.Computer)
admin.site.register(models.CPU)
admin.site.register(models.RAM)
admin.site.register(models.NIC)
admin.site.register(models.Disk)
admin.site.register(models.EventLog, EventAdmin)
admin.site.register(models.NewAssetApprovalZone, NewAssetAdmin)
