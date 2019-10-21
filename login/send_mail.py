import os
from django.core.mail import send_mail

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

if __name__ == '__main__':
    send_mail('django test mail',
              'neirong',
              'jasper_lei@huatek.com',
              ['jasper_lei@huatek.com'],
              )
