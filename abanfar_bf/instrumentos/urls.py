from django.urls import path
from . import views

app_name = "instrumentos"

urlpatterns = [
    path("", views.list_instrumentos, name="list"),
    path("cadastrar/", views.criar_instrumento, name="create"),
    path("<int:id>/atribuir/", views.atribuir_instrumento, name="atribuir"),
    path("<int:id>/uso/", views.uso_instrumento, name="uso"),
    path("<int:id>/editar/", views.editar_instrumento, name="editar"),
    path("<int:id>/excluir/", views.excluir_instrumento, name="excluir"),

    # API endpoints
    path("api/painel/", views.api_painel_geral, name="api_painel"),
    path("api/listar/", views.api_listar_instrumentos, name="api_listar"),
    path("api/buscar-rfid/<str:rfid>/", views.api_buscar_rfid, name="api_buscar_rfid"),
    path("api/retirada/", views.api_registrar_retirada, name="api_retirada"),
    path("api/devolucao/", views.api_registrar_devolucao, name="api_devolucao"),
    path("api/emprestimos/", views.api_listar_emprestimos, name="api_emprestimos"),
]
