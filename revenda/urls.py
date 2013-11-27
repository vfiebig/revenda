from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'revenda.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'crud.views.index'),
    url(r'^update/', 'crud.views.update'),
    url(r'^delete/', 'crud.views.delete'),
    

    url(r'^admin/', include(admin.site.urls)),
)


urlpatterns += patterns('',
    url(r'^crud/(?P<file_id>[0-9a-f]{24})/$', 'crud.views.serve_file'),
)

