import json

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render
from .decorators import user_sem_login, users_autorizados, user_admin, user_colaborador, user_cliente
from django.contrib.auth.models import Group

from .forms import VinhoForm, PedidoForm
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

@user_sem_login
def register(request):

    if request.user.is_authenticated:
        return redirect('home')
    else:

        if request.method == 'POST':
            username = request.POST['username']
            nome = request.POST['name']
            apelido = request.POST['lname']
            email = request.POST['email']
            telemovel = request.POST['telemovel']
            password = request.POST['password1']
            password2 = request.POST['password2']
            terms = request.POST.get('terms', "")
            plus18 = request.POST.get('plus18', "")

            if User.objects.filter(username=username):
                messages.info(request, "O Username já está em uso.")
                return redirect('register')

            if len(username) > 20:
                messages.info(request, "O Username tem de ter menos de 20 caracteres.")
                return redirect('register')

            if User.objects.filter(email=email).exists():
                messages.info(request, "O Email já está em uso.")
                return redirect('register')

            if password != password2:
                messages.info(request, "As passwords não coincidem.")
                return redirect('register')

            if not telemovel.isalnum():
                messages.info(request, "Telemóvel inválido.")
                return redirect('register')

            if not plus18:
                messages.info(request, "Tem de ser maior de idade.")
                return redirect('register')

            if not terms:
                messages.info(request, "Tem de concordar com os termos e condições.")
                return redirect('register')

            cliente = User.objects.create_user(username,email,password)
            cliente.first_name = nome
            cliente.last_name = apelido
            cliente.save()
            novo_cliente = Cliente(user=cliente,nome=nome,apelido=apelido,email=email,telemovel=telemovel)
            novo_cliente.save()
            group = Group.objects.get(name='clientes')
            cliente.groups.add(group)

            messages.success(request, "Registo completado com sucesso.")
            return redirect('loginUser')

    return render(request, 'adegadobairro/register.html')

# Create your views here.
def home(request):
    if request.user.groups.exists():
        grupo = request.user.groups.all()[0].name
    else:
        grupo = "None"
    print(grupo)
    context = {'tipo':grupo}
    return render(request, 'adegadobairro/home.html', context)

@user_sem_login
def loginUser(request):
        context = {}
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password1')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, "Username não é válido, ou a Password está errada.")
        return render(request, 'adegadobairro/login.html', context)

@login_required(login_url='loginUser')
def logoutUser(request):
        logout(request)
        if request.user.groups.exists():
            grupo = request.user.groups.all()[0].name
        else:
            grupo = "None"
        context = {'tipo': grupo}
        return render(request, 'adegadobairro/home.html', context)

@user_cliente
def minhaconta(request):
    if request.user.groups.exists():
        grupo = request.user.groups.all()[0].name
    else:
        grupo = "None"
    print(grupo)

    cliente = Cliente.objects.get(user=request.user)

    if request.method == 'POST':
        nome = request.POST['name']
        apelido = request.POST['lname']
        email = request.POST['email']
        telemovel = request.POST['telemovel']
        password = request.POST['password1']
        password2 = request.POST['password2']

        if nome != cliente.nome and nome != None and nome != "":
            cliente.nome=nome;
            u= request.user
            u.first_name=nome;
            u.save()
            cliente.save()
            messages.info(request, "Nome Alterado.")

        if apelido != cliente.apelido and apelido != None and apelido != "":
            cliente.apelido = apelido;
            u = request.user
            u.last_name = nome;
            u.save()
            cliente.save()
            messages.info(request, "Apelido Alterado.")

        if not User.objects.filter(email=email).exists() and email != cliente.email:
            u = request.user
            cliente.email=email;
            u.email=cliente.email
            cliente.save()
            u.save()
            messages.info(request, "Email Alterado.")

        if password == password2:
            try:
                u = User.objects.get(email=cliente.email)
                u.set_password(password)
                messages.info(request, "Password Alterada.")
                u.save()
            except:
                messages.info(request, "A password não foi alterada devido a erro.")


        if telemovel.isalnum() and telemovel!=cliente.telemovel :
            cliente.telemovel = telemovel;
            cliente.save()
            messages.info(request, "Telemóvel Alterado.")

    pedidos=Pedido.objects.filter(cliente=cliente,fechado=True)

    context = {"uemail":cliente.email,"usernome":cliente.nome,"userapelido":cliente.apelido,"usertelemovel":cliente.telemovel,"tipo":grupo,"pedidos":pedidos}
    return render(request, 'adegadobairro/minhaconta.html',context)

def sobre(request):
    if request.user.groups.exists():
        grupo = request.user.groups.all()[0].name
    else:
        grupo = "None"
    print(grupo)

    context = {'tipo':grupo}
    return render(request, 'adegadobairro/sobre.html', context)

def termos(request):
    if request.user.groups.exists():
        grupo = request.user.groups.all()[0].name
    else:
        grupo = "None"
    print(grupo)

    context = {'tipo': grupo}
    return render(request, 'adegadobairro/termos.html', context)

@users_autorizados
def dashboard(request):
    if request.user.groups.exists():
        grupo = request.user.groups.all()[0].name
    else:
        grupo = "None"
    print(grupo)

    context = {'tipo': grupo}
    return render(request, 'adegadobairro/maindashboard.html', context)

@user_admin
def dashboardcolab(request):
    colabs = User.objects.filter(groups__name='colabs')
    context = {'colabs':colabs}
    if request.method == 'POST':
        username = request.POST['username']
        nome = request.POST['name']
        apelido = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password1']
        password2 = request.POST['password2']

        if User.objects.filter(username=username) or username=="":
            messages.info(request, "O Username Inválido.")
            return redirect('dashboardcolab')

        if len(username) > 20:
            messages.info(request, "O Username tem de ter menos de 20 caracteres.")
            return redirect('dashboardcolab')

        if User.objects.filter(email=email).exists():
            messages.info(request, "O Email já está em uso.")
            return redirect('dashboardcolab')

        if password != password2:
            messages.info(request, "As passwords não coincidem.")
            return redirect('dashboardcolab')

        colab = User.objects.create_user(username, email, password)
        colab.save()
        colab.first_name= nome
        colab.last_name= apelido
        colab.save()
        group = Group.objects.get(name='colabs')
        colab.groups.add(group)

        messages.success(request, "Registo completado com sucesso.")
        return render(request, 'adegadobairro/dashboardcolab.html', context)
    return render(request, 'adegadobairro/dashboardcolab.html', context)

@users_autorizados
def dashboardpedidos(request):
    if request.user.groups.exists():
        grupo = request.user.groups.all()[0].name
    else:
        grupo = "None"
    pedidosa = Pedido.objects.filter(fechado=True, enviado_ou_levantado=False)
    pedidosf = Pedido.objects.filter(fechado=True, enviado_ou_levantado=True)
    context = {"tipo": grupo, 'pedidosa': pedidosa, 'pedidosf': pedidosf}
    return render(request, 'adegadobairro/dashboardpedidos.html', context)

@user_admin
def apagarcolab(request, pk):
    context = {}
    colab = User.objects.get(username=pk)
    colab.delete()

    return render(request, 'adegadobairro/dashboardcolab.html', context)

@user_admin
def editarcolab(request, pk):
    colab = User.objects.get(username=pk)

    if request.method == 'POST':
        nome = request.POST['name']
        apelido = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password1']
        password2 = request.POST['password2']

        if nome != colab.first_name and nome != None and nome != "":
            colab.first_name = nome;
            colab.save()
            messages.info(request, "Nome Alterado.")

        if apelido != colab.last_name and apelido != None and apelido != "":
            colab.last_name = apelido;
            colab.save()
            messages.info(request, "Apelido Alterado.")

        if not User.objects.filter(email=email).exists() and email != colab.email:
            colab.email = email;
            colab.save()
            messages.info(request, "Email Alterado.")

        if password == password2:
            try:
                u = User.objects.get(email=colab.email)
                u.set_password(password)
                messages.info(request, "Password Alterada.")
                u.save()
            except:
                messages.info(request, "A password não foi alterada devido a erro.")

    context = {"colab":colab}
    return render(request, 'adegadobairro/editarcolab.html', context)

@users_autorizados
def dashboardvinho(request):
    if request.user.groups.exists():
        grupo = request.user.groups.all()[0].name
    else:
        grupo = "None"
    print(grupo)

    vinhos = Vinho.objects.all()
    if request.method == 'POST':
        form = VinhoForm(request.POST, request.FILES)

        if form.is_valid():
            nome=request.POST.get('nome')
            colheita=request.POST.get('colheita')
            precopromocao = request.POST.get('precopromocao')
            tipo =  request.POST.get('tipo')
            print(precopromocao)
            try:
                Vinho.objects.get(nome=nome, colheita=colheita, tipo=tipo)
            except:
                form.save()
                v = Vinho.objects.get(nome=nome,colheita=colheita,tipo=tipo)
                if v.precopromocao == 0:
                    v.precoatual = v.preco
                else:
                    v.precoatual = v.precopromocao
                v.save()
            return redirect('dashboardvinho')

    else:
        form = VinhoForm()


    return render(request, 'adegadobairro/dashboardvinho.html', {'vinhos':vinhos,'form': form, 'tipo':grupo})

@users_autorizados
def editarvinho(request, pk):
    if request.user.groups.exists():
        grupo = request.user.groups.all()[0].name
    else:
        grupo = "None"
    print(grupo)

    vinho = Vinho.objects.get(vinho_id=pk)
    form = VinhoForm(instance=vinho)
    if request.method == 'POST':
        nome = request.POST.get('nome')
        colheita = request.POST.get('colheita')
        tipo = request.POST.get('tipo')
        form = VinhoForm(request.POST, instance=vinho)
        if form.is_valid():
            form.save()
            v = Vinho.objects.get(nome=nome, colheita=colheita, tipo=tipo)
            if v.precopromocao == 0:
                v.precoatual = v.preco
            else:
                v.precoatual = v.precopromocao
            v.save()
            return render(request, 'adegadobairro/editarvinho.html', {'form': form,'vinho':vinho,'tipo': grupo})

    if vinho.precopromocao == 0:
        vinho.precopromocao = None;
        vinho.save()

    context = {'form': form, 'vinho':vinho}
    return render(request, 'adegadobairro/editarvinho.html', context)

@user_admin
def apagarvinho(request, pk):
    print(pk)
    vinho = Vinho.objects.get(vinho_id=pk)
    vinho.delete()
    vinhos = Vinho.objects.all()
    form = VinhoForm()

    context = {'vinhos': vinhos, 'form': form}

    return render(request, 'adegadobairro/dashboardvinho.html', context)

def vinhos(request):
    if request.user.groups.exists():
        grupo = request.user.groups.all()[0].name
    else:
        grupo = "None"
    print(grupo)
    vinhos = Vinho.objects.all()
    if request.method == 'POST':
        ordenar = request.POST['ordenar']
        tipo = request.POST['tipo']
        promocoes = request.POST.get('promocoes', "off")
        pesquisa = request.POST['pesquisa']

        if promocoes == "on":
            vinhos = vinhos.filter(precopromocao__gt=0.01)

        if tipo != "":
            vinhos= vinhos.filter(tipo=tipo)

        if pesquisa != "":
            vinhos= vinhos.filter(nome__contains=pesquisa)

        print(ordenar)
        if ordenar == "preço":
            vinhos=vinhos.order_by('precoatual')

        if ordenar == "maisvendidos":
            vinhos=vinhos.order_by('-vendas')

        if ordenar == "maisrecentes":
            vinhos=vinhos.order_by('-datainsercao')


    context = {'vinhos': vinhos, 'tipo':grupo}
    return render(request, 'adegadobairro/vinhos.html', context)

def vinho(request, pk):
    if request.user.groups.exists():
        grupo = request.user.groups.all()[0].name
    else:
        grupo = "None"
    print(grupo)
    vinho = Vinho.objects.get(vinho_id=pk)
    print(pk)
    context = {'vinho': vinho, 'tipo':grupo}

    return render(request, 'adegadobairro/vinho.html', context)

@user_cliente
def checkout(request, pk):
    if request.user.groups.exists():
        grupo = request.user.groups.all()[0].name
    else:
        grupo = "None"
    print(pk)
    pedido = Pedido.objects.get(pedido_id=pk)
    form = PedidoForm(request.POST)
    if request.method == 'POST':

        if form.is_valid():
            morada = request.POST['morada']
            cidade = request.POST['cidade']
            nif = request.POST['nif']
            emloja = request.POST.get('enviooulevantamento')
            if emloja == "emcasa":
                pedido.precototal = pedido.precototal + 3.5

            pedido.nif=nif
            pedido.cidade=cidade
            pedido.morada=morada
            pedido.fechado=True
            pedido.save()
            cliente = Cliente.objects.get(user=request.user)
            if request.user.groups.exists():
                grupo = request.user.groups.all()[0].name
            else:
                grupo = "None"
            pedidos = Pedido.objects.filter(cliente=cliente, fechado=True)
            context = {"uemail": cliente.email, "usernome": cliente.nome, "userapelido": cliente.apelido,
                       "usertelemovel": cliente.telemovel, "tipo": grupo, "pedidos": pedidos}
            return render(request, 'adegadobairro/minhaconta.html',context)

    return render(request, 'adegadobairro/checkout.html', {'pedido': pedido, 'form': form, 'tipo': grupo})

@user_cliente
def cesto(request):

    if request.user.groups.exists():
        grupo = request.user.groups.all()[0].name
    else:
        grupo = "None"
    print(grupo)
    cliente=request.user.cliente
    contexto={'tipo':grupo}

    if  Pedido.objects.filter(cliente=cliente, fechado=False).count()>0:
        pedido = Pedido.objects.get(cliente=cliente, fechado=False)
        pedidos_vinhos = Pedido_Vinho.objects.filter(pedido=pedido, fechado=False)
        contexto = {'pedido':pedido.pedido_id,'pedidos_vinhos':pedidos_vinhos, 'tipo':grupo, 'total':pedido.precototal}
        if pedido.precototal == 0:
            return render(request, 'adegadobairro/vinhos.html', contexto)
        return render(request, 'adegadobairro/cesto.html', contexto)
    else:
        return render(request, 'adegadobairro/home.html', contexto)

@user_cliente
def update_item(request):
    data = json.loads(request.body)
    vinhoid = data['vinhoid']
    acao = data['acao']
    pedido_vinho = None
    print('Acao:', acao)
    print('vinhoid:', vinhoid)
    cliente=request.user.cliente
    vinho = Vinho.objects.get(vinho_id=vinhoid)
    pedido, created= Pedido.objects.get_or_create(cliente=cliente, fechado=False)
    if vinho.precopromocao > 0:
        pedido_vinho, created = Pedido_Vinho.objects.get_or_create(pedido=pedido, fechado=False, vinho=vinho,                                                     preco=vinho.precopromocao)
    else:
        pedido_vinho, created= Pedido_Vinho.objects.get_or_create(pedido=pedido, fechado=False, vinho=vinho, preco=vinho.preco)


    if acao == 'add':
        pedido_vinho.precototal=pedido_vinho.precototal + pedido_vinho.preco
        pedido_vinho.quantidade= pedido_vinho.quantidade +1
        pedido.precototal = pedido.precototal + pedido_vinho.preco
        pedido_vinho.save()
        pedido.save()

    elif acao == 'remove':
        pedido_vinho.precototal = pedido_vinho.precototal - pedido_vinho.preco
        pedido_vinho.quantidade = pedido_vinho.quantidade - 1
        pedido.precototal = pedido.precototal - pedido_vinho.preco
        pedido_vinho.save()
        pedido.save()

    if pedido_vinho.quantidade <=0:
        pedido_vinho.delete()
    return JsonResponse('Vinho adicionado.',safe=False)

@user_cliente
def pagar(request, pk):
    pedido = Pedido.objects.get(pedido_id=pk)
    pedido.pago=True
    pedido.save()
    pedidos_vinhos = Pedido_Vinho.objects.filter(pedido=pedido)
    for p in pedidos_vinhos:
        vinho= Vinho.objects.get(vinho_id=p.vinho_id)
        vinho.vendas = vinho.vendas + p.quantidade
        vinho.save()

    cliente = Cliente.objects.get(user=request.user)
    if request.user.groups.exists():
        grupo = request.user.groups.all()[0].name
    else:
        grupo = "None"
    pedidos = Pedido.objects.filter(cliente=cliente, fechado=True)
    context = {"uemail": cliente.email, "usernome": cliente.nome, "userapelido": cliente.apelido,
               "usertelemovel": cliente.telemovel, "tipo": grupo, "pedidos": pedidos}
    return render(request, 'adegadobairro/minhaconta.html', context)

@user_cliente
def cancelar(request, pk):
    pedido = Pedido.objects.get(pedido_id=pk)
    pedido.delete()
    cliente = Cliente.objects.get(user=request.user)
    if request.user.groups.exists():
        grupo = request.user.groups.all()[0].name
    else:
        grupo = "None"
    pedidos = Pedido.objects.filter(cliente=cliente, fechado=True)
    context = {"uemail": cliente.email, "usernome": cliente.nome, "userapelido": cliente.apelido,
               "usertelemovel": cliente.telemovel, "tipo": grupo, "pedidos": pedidos}
    return render(request, 'adegadobairro/minhaconta.html', context)

@users_autorizados
def cancelarloja(request, pk):
    pedido = Pedido.objects.get(pedido_id=pk)
    pedido.delete()
    if request.user.groups.exists():
        grupo = request.user.groups.all()[0].name
    else:
        grupo = "None"
    pedidosa = Pedido.objects.filter(fechado=True, enviado_ou_levantado=False)
    pedidosf = Pedido.objects.filter(fechado=True, enviado_ou_levantado=True)
    context = {"tipo": grupo, 'pedidosa': pedidosa, 'pedidosf': pedidosf}
    return render(request, 'adegadobairro/dashboardpedidos.html', context)

@users_autorizados
def preparar(request, pk):
    pedido = Pedido.objects.get(pedido_id=pk)
    pedido.pronto=True
    pedido.save()
    if request.user.groups.exists():
        grupo = request.user.groups.all()[0].name
    else:
        grupo = "None"
    pedidosa = Pedido.objects.filter(fechado=True, enviado_ou_levantado=False)
    pedidosf = Pedido.objects.filter(fechado=True, enviado_ou_levantado=True)
    context = {"tipo": grupo, 'pedidosa': pedidosa, 'pedidosf': pedidosf}
    return render(request, 'adegadobairro/dashboardpedidos.html', context)

@users_autorizados
def enviar(request, pk):

    pedido = Pedido.objects.get(pedido_id=pk)
    pedido.enviado_ou_levantado=True
    pedido.save()
    if request.user.groups.exists():
        grupo = request.user.groups.all()[0].name
    else:
        grupo = "None"
    pedidosa = Pedido.objects.filter(fechado=True, enviado_ou_levantado=False)
    pedidosf = Pedido.objects.filter(fechado=True, enviado_ou_levantado=True)
    context = {"tipo": grupo, 'pedidosa': pedidosa, 'pedidosf': pedidosf}
    return render(request, 'adegadobairro/dashboardpedidos.html', context)

@login_required(login_url='loginUser')
def verencomenda(request, pk):
    if request.user.groups.exists():
        grupo = request.user.groups.all()[0].name
    else:
        grupo = "None"
    pedido = Pedido.objects.get(pedido_id=pk)
    pedidos_vinhos = Pedido_Vinho.objects.filter(pedido=pedido)
    contexto={'pedido':pedido, 'pedidos_vinhos':pedidos_vinhos, 'tipo':grupo}
    return render(request, 'adegadobairro/verencomenda.html', contexto)
