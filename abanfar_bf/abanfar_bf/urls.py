from django.contrib import admin
from django.urls import path, include
from blog.views import home   # IMPORTA A VIEW DO BLOG

urlpatterns = [
    path('admin/', admin.site.urls),
    path('professores/', include("professores.urls")),
    path('', home, name='home'),  # ROTA PARA A PÁGINA INICIAL
    path("contas/", include("contas.urls")),
    path("alunos/", include("alunos.urls")),
    path("instrumentos/", include("instrumentos.urls")),
]

