from django.urls import path
from . import views

app_name = "grupos"

urlpatterns = [
    path("", views.lista_grupos, name="lista"),
    path("<int:id>/", views.grupo_detalhes, name="detalhes"),
    path("enviar/<int:id>/", views.enviar_partitura, name="enviar_partitura"),
    path("listar/", views.grupos_listar, name="listar"),
    path("exportar/", views.exportar_grupos_csv, name="exportar_grupos_csv"),
    path("exportar/excel/", views.exportar_grupos_excel, name="exportar_grupos_excel"),
    path("exportar/pdf/", views.exportar_grupos_pdf, name="exportar_grupos_pdf"),
    path("criar/", views.grupo_criar, name="criar"),
    path("editar/<int:id>/", views.grupo_editar, name="editar"),
    path("arquivar/<int:id>/", views.grupo_arquivar, name="arquivar"),
    path("reativar/<int:id>/", views.grupo_reativar, name="reativar"),

]