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
]
