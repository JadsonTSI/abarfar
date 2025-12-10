from django.urls import path
from . import views
from .views import perfil_view

app_name = "contas"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    #  ROTAS MAIS ESPECÍFICAS PRIMEIRO
    path("gerente/alunos/", views.lista_alunos, name="lista_alunos"),

    #  DEPOIS AS ROTAS GERAIS
    path("gerente/", views.painel_gerente, name="painel_gerente"),
    path("professor/", views.painel_professor, name="painel_professor"),
    path("aluno/", views.painel_aluno, name="painel_aluno"),
    path("perfil/", perfil_view, name="perfil"),
    path('alterar-foto/', views.alterar_foto, name="alterar_foto")


]

