from django.urls import path, include

from table.admin import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),
    path('', include('table.urls'))
]
