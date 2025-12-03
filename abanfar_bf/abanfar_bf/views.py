from django.http import HttpResponse

def teste_view(request):
    return HttpResponse('olá, mundo!')

