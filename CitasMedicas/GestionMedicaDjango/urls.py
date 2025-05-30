from django.contrib import admin
from django.urls import path, include
from AppCitas.views import home
from GestionMedicaDjango import settings
from django.conf import settings
from django.conf.urls.static import static


admin.site.site_header = 'Gestion Médica Admin'
admin.site.site_title = 'Gestión Médica'
admin.site.index_title = 'Administración del sistema de citas médicas'

urlpatterns = [
    path('', home, name='home-page'),
    path('admin/', admin.site.urls),
    path('AppCitas/', include('AppCitas.urls')),  
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('api.urls')),
    path('users/', include('users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)