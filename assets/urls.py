from django.urls import path, include
from . import views

app_name = 'assets'

urlpatterns = [
    path('report/', views.report, name='report')
]
