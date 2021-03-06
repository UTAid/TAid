from django.conf.urls import patterns, include, url
from django.contrib import admin
import rest_framework_jwt.views as jwt

from TAid.settings import common
from apps.api import viewsets
from apps.api.views import schema_view


v0_patterns = [
    url(r'^', include(viewsets.router.urls)),
    url(r'^docs/', schema_view),
]

api_patterns = [
    url(r'^v0/', include(v0_patterns)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^token-auth/', jwt.obtain_jwt_token),
    url(r'^token-refresh/', jwt.refresh_jwt_token),
    url(r'^token-verify/', jwt.verify_jwt_token),
]

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(api_patterns)),

    # Static files (images, css, javascript, etc.)
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': common.MEDIA_ROOT},
    ),
)
