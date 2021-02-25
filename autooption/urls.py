from django.conf.urls import patterns, include, url
from autooption.views import *

from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'autooption.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    (r'^$',default),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$',login,name='login'),
    url(r'^logout_user/$',logout_user,name='logout_user'),
    
    url(r'^conf/$',conf,name='conf'),
    url(r'^wl_setconf/$',wl_setconf,name='wl_setconf'),
    url(r'^op_setconf/$',op_setconf,name='op_setconf'),
    url(r'^or_setconf/$',or_setconf,name='or_setconf'),
    url(r'^my_setconf/$',my_setconf,name='my_setconf'),
    url(r'^fd_setconf/$',fd_setconf,name='fd_setconf'),
    
    url(r'^install/$',install,name='install'),
    url(r'^wl_install/$',wl_install,name='wl_install'),
    url(r'^op_install/$',op_install,name='op_install'),
    url(r'^or_install/$',or_install,name='or_install'),
    url(r'^monitor/$',monitor,name='monitor'),
    url(r'^monitor_data/$',monitor_data,name='monitor_data'),
    url(r'^watchDATA/$',watchDATA,name='watchDATA'),
    url(r'^history/$',history,name='history'),
    url(r'^monitor_historydata/$',monitor_historydata,name='monitor_historydata'),
    
    ####
    url(r'^monitor_list/$',monitor_list,name='monitor_list'),
    url(r'^monitor_get_list/$',monitor_get_list,name='monitor_get_list'),
    url(r'^monitor_host_add/$',monitor_host_add,name='monitor_host_add'),
    url(r'^monitor_host_del/$',monitor_host_del,name='monitor_host_del'),
    url(r'^monitor_singlehost_info/$',monitor_singlehost_info,name='monitor_singlehost_info'),
    url(r'^monitor_singlehost_modify/$',monitor_singlehost_modify,name='monitor_singlehost_modify'),
    url(r'^monitor_group_add/$',monitor_group_add,name='monitor_group_add'),
    url(r'^monitor_group_del/$',monitor_group_del,name='monitor_group_del'),
    
    url(r'^monitor_info/$',monitor_info,name='monitor_info'),
    url(r'^monitor_get_info/$',monitor_get_info,name='monitor_get_info'),
    ####


    url(r'^ssh_check/$',ssh_check,name='ssh_check'),
    url(r'^menu/$',menu,name='menu'),
    
    url(r'^refresh_install/$',refresh_install,name='refresh_install'),
    url(r'^checklistdata/$',checklistdata,name='checklistdata'),
    url(r'^checklist/$',checklist,name='checklist'),
    url(r'^patchReport/$',patchReport,name='patchReport'),
    url(r'^detail/$',detail,name='detail'),
    url(r'^autocheck/$',autocheck,name='autocheck'),
    url(r'^downReport/$',downReport,name='downReport'),
    url(r'^downExcel/$',downExcel,name='downExcel'),

)
