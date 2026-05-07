from django.contrib import admin
from django.urls import path, include
from blog.views import home   # IMPORTA A VIEW DO BLOG
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('professores/', include("professores.urls")),
    path('', home, name='home'),  # ROTA PARA A PÁGINA INICIAL
    path("contas/", include("contas.urls")),
    path("alunos/", include("alunos.urls")),
    path("instrumentos/", include("instrumentos.urls")),
    path("materias/", include("materias.urls")),
    path("grupos/", include("grupos.urls")),
    path('transparencia/', include('transparencia.urls', namespace='transparencia')),
 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
