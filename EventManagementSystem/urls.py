"""EventManagementSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
# from django.conf.urls import url


from django.conf import settings
from django.contrib.staticfiles.views import serve as serve_static
from django.views.decorators.cache import never_cache
from django.views.generic.base import RedirectView
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('EventWebSite.urls')),
    path('administrator/', include('Administrator.urls')),
    path('EventCommittee/', include('UserManager.urls')),
    path('eventHead/', include('EventHead.urls')),
    path('coordinator/', include('Coordinator.urls')),
    re_path(r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL+'media/favicon.ico')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += re_path(r'.+', never_cache(serve_static)),
