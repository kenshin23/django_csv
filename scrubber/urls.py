from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'scrubber.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^files/', include('scrub_csv.urls', namespace="files")),
    url(r'^admin/', include(admin.site.urls)),
]
