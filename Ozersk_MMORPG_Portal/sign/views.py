from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required



import datetime
from random import randint, seed

from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from Ozersk_MMORPG_Portal import settings
from .forms import RegistrationForm, ActivationCodeForm
from .models import Profile


def generate_code():
    seed()
    return str(randint(100000, 999999))


# Обработчик регистрации. Ввод данных
def register(request):
    if not request.user.is_authenticated:
        if request.POST:
            form = RegistrationForm(request.POST or None)
            if form.is_valid():
                user_reg = form.save(commit=False)
                user_reg.is_active = False
                form.save()

                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                my_password1 = form.cleaned_data.get('password1')
                u_f = User.objects.get(username=username, email=email, is_active=False)

                # Устанавливаем права на добавление постов и работу с комментариями
                author_group = Group.objects.get(name='authors')
                author_group.user_set.add(u_f)

                code = generate_code()

                #message = code
                message = f'Код подтверждения: {code}'
                user = authenticate(username=username, password=my_password1)
                now = datetime.datetime.now()

                Profile.objects.create(user=u_f, code=code, date=now)

                # Отправка кода в почту
                send_mail('Регистрация на Ozersk_MMORPG_Portal',
                          message,
                          settings.DEFAULT_FROM_EMAIL,
                          [email],
                          fail_silently=False)

                if user and user.is_active:
                    login(request, user)
                    #return redirect('/personalArea/')
                    return redirect('/')
                else:
                    form.add_error(None, 'Аккаунт не активирован')
                    # Форма для ввода кода
                    return redirect('../activation_code_form')
            else:
                return render(request, 'sign/register.html', {'form': form})
        else:
            return render(request, 'sign/register.html', {'form': RegistrationForm()})
    else:
        #return redirect('/personalArea/')
        return redirect('/')


# второй этап регистрации - ввод одноразового кода
def end_reg(request):
    if request.user.is_authenticated:
        #return redirect('/personalArea/')
        return redirect('/')
    else:
        if request.method == 'POST':
            form = ActivationCodeForm(request.POST)
            if form.is_valid():
                code_use = form.cleaned_data.get("code")
                if Profile.objects.filter(code=code_use):
                    # Код существует
                    profile = Profile.objects.get(code=code_use)
                else:
                    form.add_error(None, "Код подтверждения не совпадает.")
                    return render(request, 'sign/activation_code_form.html', {'form': form})
                if profile.user.is_active == False:
                    profile.user.is_active = True
                    profile.user.save()
                    user = authenticate(request, username=profile.user.username, password=profile.user.password)
                    if user is not None:
                        login(request, user)

                    profile.delete()
                    # Регистрация пройдена, переходим на страницу входа
                    return redirect('/sign/login')
                else:
                    #print('Пользователь уже активирован')
                    form.add_error(None, 'Unknown or disabled account')
                    return render(request, 'sign/activation_code_form.html', {'form': form})
            else:
                #print('Форма не валидна')
                return render(request, 'sign/activation_code_form.html', {'form': form})
        else:
            #print('запрос GET')
            form = ActivationCodeForm()
            return render(request, 'sign/activation_code_form.html', {'form': form})




class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'
    #success_url = 'activation_code_form/'


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/')



