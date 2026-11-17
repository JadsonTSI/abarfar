from django.urls import path

from . import views

app_name = "ouvidoria"

urlpatterns = [
    path("", views.ouvidoria, name="index"),
    path("enviada/", views.enviada, name="enviada"),
    path("acompanhar/", views.acompanhar, name="acompanhar"),
]
