from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/', views.post_list, name='post_list'),
    path('blog/post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('sobre/', views.sobre, name='sobre'),
    path('projetos/', views.projetos, name='projetos'),
    path('galeria/', views.galeria, name='galeria'),
    path('contato/', views.contato, name='contato'),
    path('newsletter/', views.newsletter, name='newsletter'),
]
