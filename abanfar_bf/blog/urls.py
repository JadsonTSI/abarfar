from django.contrib import admin
from django.urls import path
from blog.views import home
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('transparencia/', views.portal_transparencia,  name='transparencia'),
]
