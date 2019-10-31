from django.urls import path, include
from . import views

app_name = 'assets'

urlpatterns = [

    path('report/', views.report, name='report'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('index/', views.index, name='index'),
    path('userpage/', views.userpage, name='userpage'),
    path('assets/detail/<int:asset_id>/', views.detail, name="detail"),
    # path('', views.dashboard),
]
