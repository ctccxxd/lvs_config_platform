
from django.contrib import admin 
from django.conf.urls import * 
from django.conf import settings
from django.conf.urls import url
import settings
from . import view
 
urlpatterns = [
    url(r'^$', view.index),
    url(r'^addlvs$', view.addlvs),
    url(r'^deletelvs$', view.deletelvs),
    url(r'^findlvs$', view.findlvs),
    url(r'^chglvs$', view.chglvs),
    url(r'^admin/', include(admin.site.urls)), 
    url(r'^Remote_lvs_config/', include('Remote_lvs_config.urls')), 
    url(r'^static/(?P.*)$','django.views.static.server',{'document_root':settings.STATICFILES_DIRS},name='static'), 
]

