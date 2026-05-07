from django.urls import path
from . import views
 
app_name = 'transparencia'
 
urlpatterns = [
    path('',                      views.portal_transparencia, name='portal'),
    path('gerente/',              views.gestao_transparencia, name='gestao'),
    path('toggle/<int:doc_id>/',  views.toggle_publicacao,    name='toggle'),
    path('excluir/<int:doc_id>/', views.excluir_documento,    name='excluir'),
]
 