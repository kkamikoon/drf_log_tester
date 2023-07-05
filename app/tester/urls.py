"""tester URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

directory = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'app/../api', 'versioned')

schema_view = get_schema_view(
    openapi.Info(
        title="Test Dummy API",
        default_version='v1',
        description=f"Test Dummy API Swagger.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="rootsik1221@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

api_urls = []
version_map_dict = {}

for _path, _, _files, in os.walk(directory):
    depth = _path[len(directory) + len(os.path.sep):].count(os.path.sep)
    if _path != directory and depth == 1 and 'urls.py' in _files:
        version, api_name = _path.split(os.path.sep)[-2:]

        if not version_map_dict.get(version, None):
            version_map_dict[version] = []

        _include = 'api.versioned.{}.{}.urls'.format(version, api_name)

        api_urls.append(path(f"{version}/", include(_include)))


urlpatterns = [
    path('api/', include(api_urls)),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    version = "v1"
    base_url = f"api/{version}"

    urlpatterns += [
        re_path(r'^' + base_url + '/swagger(?P<format>\.json|\.yaml)$',
                schema_view.without_ui(cache_timeout=0), name='schema-json'),
        re_path(r'^' + base_url + '/swagger/$',
                schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'^' + base_url + '/redoc/$',
                schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]

