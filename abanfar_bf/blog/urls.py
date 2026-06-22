from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('sobre/', views.sobre, name='sobre'),
    path('projetos/', views.projetos, name='projetos'),
    path('galeria/', views.galeria, name='galeria'),
    path('contato/', views.contato, name='contato'),
]
