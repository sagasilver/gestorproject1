from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$','demo.views.ingresar', name="ingresar"),
    url(r'^privado/', 'demo.views.privado', name="privado"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^cerrar/', 'demo.views.cerrar', name="cerrar"),
    url(r'^logout/$','django.contrib.auth.views.logout_then_login',name='logout'),
    url(r'^usuario/', include('sgpa.urls', namespace='usuario'))

)
