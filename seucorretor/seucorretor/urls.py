from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',  # noqa

    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^signup/', include('signup.urls')),

    url(r'^', include('core.urls')),
    url(r'^', include('pclientes.urls')),
    url(r'^', include('pcorretor.urls')),
    url(r'^atividades/', include('atividades.urls')),
    url(r'^tracking/', include('tracking.urls')),
    url(r'^relatorios/', include('relatorios.urls')),
    url(r'^vivareal/', include('vivareal.urls')),
    url(r'^zapimoveis/', include('zapimoveis.urls')),
    url(r'^buscador/', include('ibuscador.urls')),
    url(r'^buscacep/', include('buscacep.urls')),
    url(r'^imobiliaria/', include('imobiliaria.urls')),
    url(r'^crm/', include('crm.urls')),
    url(r'^cidades/', include('cidades.urls')),
    url(r'^imoveis/', include('imoveis.urls')),
    url(r'^autoatendimento/', include('autoatendimento.urls')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

# django-debug-toolbar
#if settings.DEBUG:
#    import debug_toolbar
#    urlpatterns += patterns('',  # noqa
#        url(r'^__debug__/', include(debug_toolbar.urls)),
#    )
