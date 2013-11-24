from django.conf.urls import patterns, url
from modulemanager.views import ModuleView, InstallModuleView
urlpatterns = patterns('',
                       url(r'^$', ModuleView.as_view(), name='all_modules'),
                       url(r'^install/(?P<module_id>\d+)/$', InstallModuleView.as_view(), name='install_module'),
                )