from django.shortcuts import redirect
from functools import wraps

def gerente_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('contas:login')
        try:
            perfil = request.user.perfil
            if perfil.tipo == 'gerente':
                return view_func(request, *args, **kwargs)
        except Exception:
            pass
        return redirect('contas:login')
    return _wrapped_view

def professor_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('contas:login')
        try:
            perfil = request.user.perfil
            if perfil.tipo == 'professor':
                return view_func(request, *args, **kwargs)
        except Exception:
            pass
        return redirect('contas:login')
    return _wrapped_view

def aluno_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('contas:login')
        try:
            perfil = request.user.perfil
            if perfil.tipo == 'aluno':
                return view_func(request, *args, **kwargs)
        except Exception:
            pass
        return redirect('contas:login')
    return _wrapped_view

def gerente_ou_professor_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('contas:login')
        try:
            perfil = request.user.perfil
            if perfil.tipo in ['gerente', 'professor']:
                return view_func(request, *args, **kwargs)
        except Exception:
            pass
        return redirect('contas:login')
    return _wrapped_view

def iot_api_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # 1. Se o usuário já estiver autenticado por sessão (ex: navegador), permite
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)

        # 2. Caso contrário, verifica a chave de API (X-API-KEY ou api_key)
        from django.conf import settings
        from django.http import JsonResponse
        import json

        token = request.headers.get('X-API-KEY') or request.META.get('HTTP_X_API_KEY')
        if not token:
            if request.method == 'POST':
                try:
                    body = json.loads(request.body)
                    token = body.get('api_key')
                except:
                    token = request.POST.get('api_key')
            else:
                token = request.GET.get('api_key')

        expected_token = getattr(settings, 'IOT_API_KEY', None)
        if not expected_token or token != expected_token:
            return JsonResponse({"erro": "Acesso nao autorizado. Chave de API invalida ou ausente."}, status=401)

        return view_func(request, *args, **kwargs)
    return _wrapped_view
