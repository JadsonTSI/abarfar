from django.urls import path
from . import views

app_name = "grupos"

urlpatterns = [
    path("", views.lista_grupos, name="listar"),
    path("<int:id>/", views.grupo_detalhes, name="detalhes"),
    path("enviar/<int:id>/", views.enviar_partitura, name="enviar_partitura"),
    path("listar/", views.grupos_listar, name="listar"),
    path("criar/", views.grupo_criar, name="criar"),
    path("editar/<int:id>/", views.grupo_editar, name="editar"),
    path("arquivar/<int:id>/", views.grupo_arquivar, name="arquivar"),
    path("reativar/<int:id>/", views.grupo_reativar, name="reativar"),

]