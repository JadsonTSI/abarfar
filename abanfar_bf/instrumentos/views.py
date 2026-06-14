from django.shortcuts import render, redirect, get_object_or_404
from .models import Instrumento, InstrumentoEmprestimo
from .forms import InstrumentoForm, InstrumentoEmprestimoForm

# LISTAR INSTRUMENTOS
def list_instrumentos(request):
    instrumentos = Instrumento.objects.all()
    return render(request, "instrumentos/list.html", {"instrumentos": instrumentos})

# CADASTRAR INSTRUMENTO
def criar_instrumento(request):
    if request.method == "POST":
        form = InstrumentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("instrumentos:list")
    else:
        form = InstrumentoForm()

    return render(request, "instrumentos/form.html", {"form": form})

# ATRIBUIR / EMPRESTAR INSTRUMENTO
def atribuir_instrumento(request, id):
    instrumento = get_object_or_404(Instrumento, id=id)

    if request.method == "POST":
        form = InstrumentoEmprestimoForm(request.POST)
        if form.is_valid():
            emprestimo = form.save(commit=False)
            emprestimo.instrumento = instrumento
            emprestimo.save()
            return redirect("instrumentos:list")
    else:
        form = InstrumentoEmprestimoForm()

    return render(request, "instrumentos/atribuir.html", {
        "form": form,
        "instrumento": instrumento
    })

# USO / HISTÓRICO DE EMPRESTIMOS
def uso_instrumento(request, id):
    instrumento = get_object_or_404(Instrumento, id=id)
    usos = InstrumentoEmprestimo.objects.filter(instrumento=instrumento)

    return render(request, "instrumentos/uso.html", {
        "instrumento": instrumento,
        "usos": usos
    })


def editar_instrumento(request, id):
    instrumento = get_object_or_404(Instrumento, id=id)
    
    if request.method == "POST":
        form = InstrumentoForm(request.POST, instance=instrumento)
        if form.is_valid():
            form.save()
            return redirect("instrumentos:list")
    else:
        form = InstrumentoForm(instance=instrumento)

    return render(request, "instrumentos/editar.html", {"form": form, "instrumento": instrumento})


def excluir_instrumento(request, id):
    instrumento = get_object_or_404(Instrumento, id=id)

    if request.method == "POST":
        instrumento.delete()
        return redirect("instrumentos:list")

    return render(request, "instrumentos/excluir.html", {"instrumento": instrumento})


# ── ENDPOINTS DE API PARA O APLICATIVO ─────────────────────────────────────────

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json

@csrf_exempt
def api_painel_geral(request):
    # Total de instrumentos
    total_inst = Instrumento.objects.count()
    ativos_inst = Instrumento.objects.filter(ativo=True).count()
    inativos_inst = Instrumento.objects.filter(ativo=False).count()
    
    # Contagem de empréstimos
    emprestados_ids = InstrumentoEmprestimo.objects.filter(devolvido=False).values_list('instrumento_id', flat=True)
    emprestados_count = len(emprestados_ids)
    disponiveis_count = Instrumento.objects.filter(ativo=True).exclude(id__in=emprestados_ids).count()
    
    hoje = timezone.now().date()
    vencidos_count = 0
    prestamos_ativos = InstrumentoEmprestimo.objects.filter(devolvido=False)
    for p in prestamos_ativos:
        dias = (hoje - p.data_emprestimo).days
        if dias > 14:
            vencidos_count += 1
            
    ativos_prestamos = prestamos_ativos.count() - vencidos_count
    devolvidos_prestamos = InstrumentoEmprestimo.objects.filter(devolvido=True).count()
    total_prestamos = InstrumentoEmprestimo.objects.count()
    
    # Estatísticas de Alunos
    from alunos.models import Aluno, Naipe
    total_alunos = Aluno.objects.count()
    naipes = Naipe.objects.all()
    naipes_dict = {}
    for n in naipes:
        naipes_dict[n.nome] = Aluno.objects.filter(naipe=n).count()
        
    # Estatísticas de Ensaios
    from professores.models import EnsaiosproModel
    total_ensaios = EnsaiosproModel.objects.count()
    ativos_ensaios = EnsaiosproModel.objects.filter(cancelado=False).count()
    cancelados_ensaios = EnsaiosproModel.objects.filter(cancelado=True).count()
    
    # Lista de alertas
    alertas = []
    # Alertas de vencidos
    for p in prestamos_ativos:
        dias = (hoje - p.data_emprestimo).days
        if dias > 14:
            alertas.append({
                "id": f"v-{p.id}",
                "grave": True,
                "msg": f"Prazo vencido: {p.instrumento.nome} — {p.aluno.nome} (+{dias - 14} dias)"
            })
    # Devoluções recentes
    devolvidos_recentes = InstrumentoEmprestimo.objects.filter(devolvido=True).order_by('-data_devolucao')[:3]
    for r in devolvidos_recentes:
        alertas.append({
            "id": f"d-{r.id}",
            "grave": False,
            "msg": f"{r.instrumento.nome} devolvido por {r.aluno.nome}"
        })
    # Próximos ensaios hoje/amanhã
    ensaios_hoje = EnsaiosproModel.objects.filter(data__gte=hoje, cancelado=False).order_by('data', 'inicio')[:3]
    for e in ensaios_hoje:
        dia_str = "Hoje" if e.data == hoje else e.data.strftime("%d/%m/%Y")
        alertas.append({
            "id": f"e-{e.id}",
            "grave": False,
            "msg": f"Ensaio {e.nome} {dia_str} às {e.inicio.strftime('%H:%M')} — {e.local}"
        })
        
    # Próximo ensaio em destaque
    prox_e = EnsaiosproModel.objects.filter(data__gte=hoje, cancelado=False).order_by('data', 'inicio').first()
    prox_ensaio_data = None
    if prox_e:
        dia_str = "Hoje" if prox_e.data == hoje else prox_e.data.strftime("%d/%m/%Y")
        prox_ensaio_data = {
            "nome": prox_e.nome,
            "data": prox_e.data.strftime("%d/%m/%Y"),
            "inicio": prox_e.inicio.strftime("%H:%M"),
            "local": prox_e.local,
            "dia": dia_str
        }
        
    return JsonResponse({
        "instrumentos": {
            "total": total_inst,
            "disponiveis": disponiveis_count,
            "emprestados": emprestados_count,
            "inativos": inativos_inst,
            "pertence_assoc": Instrumento.objects.filter(pertence_associacao=True).count()
        },
        "emprestimos": {
            "ativos": ativos_prestamos,
            "vencidos": vencidos_count,
            "devolvidos": devolvidos_prestamos,
            "total": total_prestamos
        },
        "alunos": {
            "total": total_alunos,
            "naipes": naipes_dict
        },
        "ensaios": {
            "total": total_ensaios,
            "ativos": ativos_ensaios,
            "cancelados": cancelados_ensaios
        },
        "alertas": alertas,
        "proximo_ensaio": prox_ensaio_data
    })


def api_listar_instrumentos(request):
    instrumentos = Instrumento.objects.all()
    data = []
    
    emprestimos_ativos = {
        emp.instrumento_id: emp
        for emp in InstrumentoEmprestimo.objects.filter(devolvido=False).select_related('aluno')
    }
    
    for inst in instrumentos:
        emprestimo = emprestimos_ativos.get(inst.id)
        disponivel = emprestimo is None
        emprestado_para = f"{emprestimo.aluno.nome} {emprestimo.aluno.sobrenome}" if emprestimo else None
        
        naipe_rel = inst.naipes.first()
        naipe_nome = naipe_rel.nome if naipe_rel else "Sem Naipe"
        
        data.append({
            "id": inst.id,
            "identificador": inst.identificador,
            "nome": inst.nome,
            "naipe": naipe_nome,
            "rfid": inst.rfid,
            "disponivel": disponivel,
            "ativo": inst.ativo,
            "pertence_associacao": inst.pertence_associacao,
            "emprestado_para": emprestado_para,
            "condicao": inst.condicao
        })
        
    return JsonResponse(data, safe=False)


def api_buscar_rfid(request, rfid):
    try:
        inst = Instrumento.objects.get(rfid=rfid)
    except Instrumento.DoesNotExist:
        return JsonResponse({"erro": "Instrumento nao encontrado"}, status=404)
        
    emprestimo = InstrumentoEmprestimo.objects.filter(instrumento=inst, devolvido=False).first()
    disponivel = emprestimo is None
    emprestado_para = f"{emprestimo.aluno.nome} {emprestimo.aluno.sobrenome}" if emprestimo else None
    
    naipe_rel = inst.naipes.first()
    naipe_nome = naipe_rel.nome if naipe_rel else "Sem Naipe"
    
    return JsonResponse({
        "id": inst.id,
        "identificador": inst.identificador,
        "nome": inst.nome,
        "naipe": naipe_nome,
        "rfid": inst.rfid,
        "disponivel": disponivel,
        "ativo": inst.ativo,
        "pertence_associacao": inst.pertence_associacao,
        "emprestado_para": emprestado_para,
        "condicao": inst.condicao
    })


@csrf_exempt
def api_registrar_retirada(request):
    if request.method == "POST":
        try:
            if request.content_type == 'application/json':
                body = json.loads(request.body)
                rfid = body.get('rfid')
                aluno_id = body.get('aluno_id')
            else:
                rfid = request.POST.get('rfid')
                aluno_id = request.POST.get('aluno_id')
                
            from alunos.models import Aluno
            inst = Instrumento.objects.get(rfid=rfid)
            aluno = Aluno.objects.get(id=aluno_id)
            
            if InstrumentoEmprestimo.objects.filter(instrumento=inst, devolvido=False).exists():
                return JsonResponse({"erro": "Instrumento ja esta emprestado"}, status=400)
                
            emprestimo = InstrumentoEmprestimo.objects.create(
                instrumento=inst,
                aluno=aluno,
                data_emprestimo=timezone.now().date(),
                devolvido=False
            )
            return JsonResponse({
                "sucesso": True,
                "msg": "Retirada registrada com sucesso",
                "id": emprestimo.id
            })
        except Instrumento.DoesNotExist:
            return JsonResponse({"erro": "Instrumento com esta tag nao cadastrado"}, status=404)
        except Aluno.DoesNotExist:
            return JsonResponse({"erro": "Aluno nao encontrado"}, status=404)
        except Exception as e:
            return JsonResponse({"erro": str(e)}, status=500)
            
    return JsonResponse({"erro": "Metodo nao permitido"}, status=405)


@csrf_exempt
def api_registrar_devolucao(request):
    if request.method == "POST":
        try:
            if request.content_type == 'application/json':
                body = json.loads(request.body)
                rfid = body.get('rfid')
            else:
                rfid = request.POST.get('rfid')
                
            inst = Instrumento.objects.get(rfid=rfid)
            emprestimo = InstrumentoEmprestimo.objects.filter(instrumento=inst, devolvido=False).first()
            
            if not emprestimo:
                return JsonResponse({"erro": "Nenhum emprestimo ativo encontrado para este instrumento"}, status=404)
                
            emprestimo.devolvido = True
            emprestimo.data_devolucao = timezone.now().date()
            emprestimo.save()
            
            return JsonResponse({
                "sucesso": True,
                "msg": "Devolucao registrada com sucesso",
                "id": emprestimo.id
            })
        except Instrumento.DoesNotExist:
            return JsonResponse({"erro": "Instrumento nao cadastrado"}, status=404)
        except Exception as e:
            return JsonResponse({"erro": str(e)}, status=500)
            
    return JsonResponse({"erro": "Metodo nao permitido"}, status=405)


def api_listar_emprestimos(request):
    emprestimos = InstrumentoEmprestimo.objects.all().select_related('instrumento', 'aluno').order_by('-data_emprestimo')
    data = []
    hoje = timezone.now().date()
    
    for emp in emprestimos:
        dias_atraso = 0
        if not emp.devolvido:
            dias = (hoje - emp.data_emprestimo).days
            if dias > 14:
                dias_atraso = dias - 14
                
        data.append({
            "id": emp.id,
            "instrumento": emp.instrumento.nome,
            "identificador": emp.instrumento.identificador,
            "rfid": emp.instrumento.rfid,
            "aluno": f"{emp.aluno.nome} {emp.aluno.sobrenome}",
            "matricula": emp.aluno.matricula,
            "data_emprestimo": emp.data_emprestimo.strftime("%d/%m/%Y"),
            "data_devolucao": emp.data_devolucao.strftime("%d/%m/%Y") if emp.data_devolucao else None,
            "devolvido": emp.devolvido,
            "dias_atraso": dias_atraso
        })
        
    return JsonResponse(data, safe=False)
