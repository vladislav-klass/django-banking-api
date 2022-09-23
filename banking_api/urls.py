"""banking_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.urlpatterns import format_suffix_patterns

from banking_api import views

schema_view = get_schema_view(
   openapi.Info(
      title="Entrix Banking API",
      default_version='v1',
      description="This is the entrix banking API",
    #   terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="vladislavklass@web.de"),
      license=openapi.License(name="Test License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', views.account_list),
    path('accounts/<int:id>/balance', views.account_balance),
    path('accounts/<int:id>/transfers', views.account_transfers),
    path('customers/', views.customer_list),
    path('transfers/', views.transfer_list),
    path('swagger(<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
