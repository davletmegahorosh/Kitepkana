from django.shortcuts import render, redirect
from django.contrib import messages
from validate_email import validate_email
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
import threading


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def send_action_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Активируйте свой аккаунт!'
    email_body = render_to_string('users/activate.html', {
        'user':user,
        'domain':current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':generate_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                 from_email=settings.EMAIL_FROM_USER,
                 to=[user.email]
                 )

    if not settings.TESTING:
        EmailThread(email).start()


def registration(request):
    if request.method == "POST":
        context = {'error': False, 'data':request.POST}
        # data.request для html, если ник уже ввели, то когда пользователь обратно войдет - введенные данны были сохранены
        # data.username; data.email и т. д.
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if len(password1) < 6:
            messages.add_message(request, messages.ERROR,
                                 'Пароль должен быть длинной не менее 6 символов!')
            context['error'] = True

        if password1 != password2:
            messages.add_message(request, messages.ERROR,
                                 'Пароли не совпадают!')
            context['error'] = True

        if not validate_email(email):
            messages.add_message(request, messages.ERROR,
                                 'Введите корректный адрес электронной почты!')
            context['error'] = True

        if not username:
            messages.add_message(request, messages.ERROR,
                                 'Введите имя пользователя!')
            context['error'] = True

        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR,
                                 'Данный пользователь с таким именем уже существует!')
            context['error'] = True

        if User.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR,
                                 'Данная почта уже используется существующим пользователем!')
            context['error'] = True

        if not context['error']:
            return render(request, '', context) #html файл внутри ковычек

        user = User.objects.create_user(username=username, email=email)
        user.set_password(password1)
        user.save()

        send_action_email(user, request)

        messages.add_message(request, messages.SUCCESS,
                             'Вам пришло письмо на почту с подтверждением!')
        return redirect('authorization')

    return render (request, '') #html файл внутри ковычек для регистрации


def authorization(request):
    if request.method == 'POST':
        context = {'data':request.POST}
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        user = authenticate(request, username=username, password1=password1)

        if not user.is_email_verified:
            messages.add_message(request, messages.ERROR,
                                 'Ваша почта не подтверждена, проверьте свою почту!')
            return render(request, '', context)

        if not user:
            messages.add_message(request, messages.ERROR,
                                 'Введены неверные данные пользователя')
            return render(request, '', context)

        login(request, user)

        messages.add_message(request, messages.SUCCESS,
                             f'Добро пожаловать {username}!')
        return redirect(reverse('home'))

    return render(request, '') #html файл внутри ковычек для авторизации


def logout_user(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS,
                         'Вы успешно вышли из аккаунта!')
    return redirect(reverse('authorization'))


def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))

        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified=True
        user.save()

        messages.add_message(request, messages.SUCCESS,
                             'Вы успешно подтвердили почту, войдите в аккаунт снова!')
        return redirect(reverse('login'))

    return render(request, 'users/activate-failed.html', {"user":user})

