from django.urls import path
from . import views

app_name = "grupos"

urlpatterns = [
    path("", views.lista_grupos, name="listar"),
    path("<int:id>/", views.grupo_detalhes, name="detalhes"),
    path("enviar/<int:id>/", views.enviar_partitura, name="enviar_partitura"),

]