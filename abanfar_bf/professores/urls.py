from django.urls import path
from . import views

app_name = "professores"

urlpatterns = [
    path("", views.professores_home, name="professoreshome"),
    path("login/", views.professores_login),
    path("ensaios/", views.ensaios_list, name="ensaios_list"),
    path("ensaios/novo/", views.ensaios_create, name="ensaios_create"),
    path("ensaios/editar/<int:id>/", views.ensaios_edit, name="ensaios_edit"),
    path("ensaios/deletar/<int:id>/", views.ensaios_delete, name="ensaios_delete"),

    # opcional: redirecionar a rota antiga
    path("ensaiospro/", views.ensaios_list, name="ensaiospro"),

    path("apresentacoes/", views.apresentacoes_list, name="apresentacoes_list"),
    path("apresentacoes/novo/", views.apresentacoes_create, name="apresentacoes_create"),
    path("apresentacoes/editar/<int:id>/", views.apresentacoes_edit, name="apresentacoes_edit"),
    path("apresentacoes/deletar/<int:id>/", views.apresentacoes_delete, name="apresentacoes_delete"),
    path("ensaios/", views.lista_ensaios_professor, name="ensaios_professor"),
    path("ensaios/<int:id>/cancelar/", views.cancelar_ensaio, name="cancelar_ensaio"),
    path("ensaios/<int:id>/restaurar/", views.restaurar_ensaio, name="restaurar_ensaio"),
    path("professores/", views.professores_list, name="professores_list"),
    path("professores/novo/", views.professores_create, name="professores_create"),
    path("professores/editar/<int:id>/", views.professores_edit, name="professores_edit"),
    path("professores/excluir/<int:id>/", views.professores_delete, name="professores_delete"),
    path("naipes/", views.naipes_view, name="naipes"),
    path("naipes/<str:nome>/", views.naipe_detalhe, name="naipe_detalhe"),
]
