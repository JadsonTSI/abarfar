from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Post
from datetime import date

def popular_posts():
    if Post.objects.count() == 0:
        Post.objects.create(
            titulo="Fundação e trajetória da ABANFAR BF",
            tag="Nossa História",
            resumo="Fundada em 2014, a ABANFAR BF é uma associação sem fins lucrativos que oferece iniciação musical, educação e inclusão social por meio de bandas, fanfarras, orquestras e projetos comunitários que transformam realidades.",
            conteudo="A Associação de Bandas, Fanfarras e Regentes de Baía Formosa/RN (ABANFAR BF) iniciou suas atividades no ano de 2014 com o firme propósito de transformar vidas através da música.\n\nAo longo de sua trajetória, a associação tem se consolidado como um farol de esperança e oportunidade para crianças e jovens de toda a região, oferecendo educação musical de qualidade totalmente gratuita.\n\nNossa missão vai além do ensino técnico instrumental; buscamos formar cidadãos conscientes, promovendo a disciplina, a colaboração em equipe, o respeito mútuo e a autoestima. Ao integrar nossos alunos em bandas e corporações musicais, oferecemos uma alternativa construtiva ao tempo ocioso, promovendo a inclusão social e combatendo a vulnerabilidade socioeconômica.\n\nAo celebrar nossa caminhada, olhamos para trás com gratidão a todos os regentes, professores, apoiadores e famílias que tornaram esse sonho possível, e seguimos com os olhos no futuro, prontos para expandir nosso alcance e continuar espalhando melodias de transformação social por Baía Formosa.",
            imagem_estatica="img/post1.jpeg",
            data_publicacao=date(2025, 5, 31)
        )
        Post.objects.create(
            titulo="Banda Musical Francisco Magalhães",
            tag="Projetos",
            resumo="A banda trabalha cidadania, sensibilidade e habilidades artísticas, reunindo jovens em um ambiente de disciplina e amor à música.",
            conteudo="A Banda Musical Francisco Magalhães é uma das principais corporações de nossa associação, reunindo dezenas de jovens instrumentistas de Baía Formosa.\n\nAtravés de ensaios regulares e apresentações públicas, o projeto foca no desenvolvimento da cidadania, sensibilidade estética e técnica instrumental. O ambiente de disciplina cooperativa estimula o senso de responsabilidade e o amor pela arte.\n\nA banda tem se apresentado em diversos eventos cívicos, festivais e encontros de bandas no Rio Grande do Norte, sendo um orgulho para a nossa comunidade.",
            imagem_estatica="img/post2.jpg",
            data_publicacao=date(2025, 4, 12)
        )
        Post.objects.create(
            titulo="Orquestra de Flautas Doce",
            tag="Orquestra",
            resumo="Projeto voltado para musicalização de crianças e adolescentes, utilizando a flauta doce como instrumento inicial.",
            conteudo="A Orquestra de Flautas Doce desempenha um papel fundamental na fase inicial de musicalização infantil na ABANFAR BF.\n\nUtilizando a flauta doce como ferramenta pedagógica por sua acessibilidade e facilidade inicial de aprendizado, o projeto introduz conceitos básicos de teoria musical, leitura de partituras e percepção rítmica.\n\nCrianças e adolescentes descobrem a alegria de tocar em grupo e desenvolvem a coordenação motora e concentração, preparando-se para integrar as corporações de metais e percussão futuramente.",
            imagem_estatica="img/post3.jpeg",
            data_publicacao=date(2025, 3, 20)
        )
        Post.objects.create(
            titulo="Apresentação na Praça Central",
            tag="Notícias",
            resumo="Nossa banda realizou apresentação especial para a comunidade, celebrando o aniversário de Baía Formosa com muita música e emoção.",
            conteudo="Para celebrar o aniversário de emancipação política de Baía Formosa, os alunos da ABANFAR BF realizaram uma apresentação memorável na Praça Central.\n\nO público presente pôde prestigiar um repertório variado, que mesclou clássicos da MPB, hinos tradicionais e arranjos de música pop contemporânea, todos executados com precisão e entusiasmo pelas corporações.\n\nO evento reforça a importância da nossa associação como polo de fomento cultural ativo e gratuito na cidade, aproximando a música da vida de cada cidadão.",
            imagem_estatica="",
            data_publicacao=date(2025, 2, 5)
        )
        Post.objects.create(
            titulo="Filarmônica encerra semestre com concerto",
            tag="Projetos",
            resumo="A Orquestra Filarmônica encerrou o primeiro semestre com concerto especial aberto à comunidade.",
            conteudo="Com o objetivo de apresentar os avanços técnicos dos alunos, a Orquestra Filarmônica realizou o Concerto de Encerramento do Semestre.\n\nO repertório contou com peças sinfônicas complexas e solos marcantes de alguns de nossos estudantes de destaque. O público compareceu em peso e aplaudiu de pé o trabalho conjunto dos músicos, professores e maestros.\n\nEste encerramento coroa o esforço de todos durante a primeira metade do ano letivo e demonstra a força transformadora da educação musical contínua.",
            imagem_estatica="",
            data_publicacao=date(2025, 1, 18)
        )

def home(request):
    popular_posts()
    posts = Post.objects.order_by('-data_publicacao')
    featured_post = posts.first() if posts.exists() else None
    grid_posts = list(posts[1:]) if posts.count() > 1 else []
    
    context = {
        'featured_post': featured_post,
        'grid_posts': grid_posts,
    }
    return render(request, "blog/home.html", context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    recent_posts = Post.objects.exclude(id=post.id).order_by('-data_publicacao')[:4]
    return render(request, "blog/post_detail.html", {"post": post, "recent_posts": recent_posts})

def sobre(request):
    return render(request, "blog/sobre.html")

def projetos(request):
    return render(request, "blog/projetos.html")

def galeria(request):
    return render(request, "blog/galeria.html")

def contato(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        assunto = request.POST.get("assunto")
        mensagem = request.POST.get("mensagem")
        messages.success(request, f"Obrigado, {nome}! Sua mensagem foi enviada com sucesso e responderemos em breve.")
    return render(request, "blog/contato.html")