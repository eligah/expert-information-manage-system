from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^$', login, name='login'),
    url(r'^register/', register, name='register'),
    url(r'^index/', index, name='index'),
    url(r'^enter_info/', enter_info, name='enter_info'),
    url(r'^change_password/', change_password, name='change_password'),
    url(r'^checkcode/', check_code, name='check_code'),
    url(r'^photo/', photo, name='photo'),
    url(r'^logout/', logout, name='logout'),
    url(r'^mindex/', mindex, name='mindex'),
    url(r'^mcolumn/', mcolumn, name='mcolumn'),
    url(r'^mdetail/$', mdetail, name='mdetail'),
    url(r'^mdetail/m_acc/$', m_acc, name='m_acc'),
    url(r'^mdetail/m_rej/$', m_rej, name='m_rej'),
    url(r'^mdetail/m_end/$', m_end, name='m_end'),
    url(r'^mchangepsw/', mchangepsw, name='mchangepsw'),
]
