from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
from .views import perfil_view

app_name = "contas"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("gerente/alunos/exportar/", views.exportar_alunos_csv, name="exportar_alunos_csv"),
    path("gerente/alunos/exportar/excel/", views.exportar_alunos_excel, name="exportar_alunos_excel"),
    path("gerente/alunos/exportar/pdf/", views.exportar_alunos_pdf, name="exportar_alunos_pdf"),
    path("gerente/alunos/", views.lista_alunos, name="lista_alunos"),

    #  DEPOIS AS ROTAS GERAIS
    path("gerente/", views.painel_gerente, name="painel_gerente"),
    path("professor/", views.painel_professor, name="painel_professor"),
    path("aluno/", views.painel_aluno, name="painel_aluno"),
    path("perfil/", perfil_view, name="perfil"),
    path('api/login/', views.login_api, name='login_api'),
    path('alterar-foto/', views.alterar_foto, name="alterar_foto"),

    # Recuperação de Senha (Forgot Password)
    path("password_reset/", auth_views.PasswordResetView.as_view(
        template_name="contas/password_reset_form.html",
        email_template_name="contas/password_reset_email.html",
        success_url=reverse_lazy("contas:password_reset_done")
    ), name="password_reset"),
    
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="contas/password_reset_done.html"
    ), name="password_reset_done"),
    
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="contas/password_reset_confirm.html",
        success_url=reverse_lazy("contas:password_reset_complete")
    ), name="password_reset_confirm"),
    
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
        template_name="contas/password_reset_complete.html"
    ), name="password_reset_complete"),
]

