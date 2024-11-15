from django.shortcuts import render
from .models import *
from .forms import UserRegister


# Create your views here.
def main_page(request):
    title = 'Главная страница'
    context = {
        "title": title
    }
    return render(request, "main_page.html", context)


def basket_page(request):
    title = 'Корзина'
    context = {
        "title": title
    }
    return render(request, "basket.html", context)


def shop_page(request):
    title = 'Перечень игр, доступных для предзаказа'
    games = Game.objects.all()

    context = {
        'title': title,
        'games': games,
    }
    return render(request, "shop.html", context)


def sign_up_by_django(request):
    info = {

    }
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = form.cleaned_data['age']
            users = Buyer.objects.values_list('name', flat=True)

            if password != repeat_password:
                info['error'] = 'Пароли не совпадают'
            elif int(age) < 18:
                info['error'] = 'Вы должны быть старше 18'
            elif username in users:
                info['error'] = 'Пользователь уже существует'
            else:
                Buyer.objects.create(name=username, balance=0.00, age=age)
                info['message'] = f'Приветствуем, {username}!'
    else:
        form = UserRegister()
        info['message'] = form

    return render(request, 'registration_page.html', context=info)


def sign_up_by_html(request):
    info = {
    }
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        age = request.POST.get('age')
        users_info = Buyer.objects.all()
        users = [user.name for user in users_info]

        if password == repeat_password and int(age) >= 18 and username not in users:
            Buyer.objects.create(name=username, balance=0.00, age=age)
            info['message'] = f"Приветствуем, {username}!"
        elif password != repeat_password:
            info['error'] = 'Пароли не совпадают'
        elif int(age) < 18:
            info['error'] = 'Вы должны быть старше 18'
        elif username in users:
            info['error'] = 'Пользователь уже существует'

    return render(request, "registration_page.html", context=info)
