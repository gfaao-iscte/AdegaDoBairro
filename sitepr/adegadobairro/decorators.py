from django.http import HttpResponse
from django.shortcuts import redirect

def user_sem_login(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

def users_autorizados(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            print("YO")
            group = request.user.groups.all()[0].name
        if group != 'admins' and group != 'colabs':
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

def user_admin(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group != 'admins':
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def user_colaborador(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group != 'colabs':
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def user_cliente(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group != 'clientes':
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
