"""main URL Configuration

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
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from accounts import urls as account_urls
from department import urls as department_urls
from main import settings
from statistic import urls as statistic_urls
from collection import urls as collection_urls
from store import urls as store_urls

urlpatterns = [
    path(
        "api/",
        include(
            [
                path("admin/", admin.site.urls),
                path("user/", include(account_urls)),
                path("department/", include(department_urls)),
                path("statistic/", include(statistic_urls)),
                path("collection/", include(collection_urls)),
                path("store/", include(store_urls)),
            ]
        ),
    )
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
