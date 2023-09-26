import random

from django.contrib.auth import login
from django.core.mail import send_mail
from django.db import models

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


from django.db import models

from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import SignupForm

from django.contrib.auth.models import User
from django import forms


#Таблица для хранения кодов регистрации
class Profile(models.Model):
    user = models.ForeignKey(User, related_name='profile', default=None, on_delete=models.CASCADE)
    code = models.CharField(max_length=50, blank=True, null=True, default=None)
    date = models.DateField(blank=True, null=True)


class EmailVerification(models.Model):
    code = models.CharField(max_length=6, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    is_verified_email = models.BooleanField(default=False)

    def __str__(self):
        return f'Подтверждение Email для {self.user.email}'

    def send_verification_email(self):
        send_mail(
            'Регистрация на Ozersk_MMORPG_Portal',
            f'Код подтверждения: {self.code}',
            'kir2845.1@yandex.ru',
            [self.user.email],
            fail_silently=False,

        )



class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )

#    def save(self, commit=True):
#        user = super(BaseRegisterForm, self).save(commit=True)
#        record = EmailVerification.objects.create(code=random.randint(100_000, 999_999), user=user)
#        record.send_verification_email()
#        return user


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
#        basic_group = Group.objects.get(name='common')
 #       basic_group.user_set.add(user)
        return user


class ActivationCodeForm(forms.Form):
    error_css_class = 'has-error'
    error_messages = {'password_incorrect':
                          ("Старый пароль не верный. Попробуйте еще раз."),
                      'password_mismatch':
                          ("Пароли не совпадают."),
                      'cod-no':
                          ("Код не совпадает."),}


    def __init__(self, *args, **kwargs):
        super(ActivationCodeForm, self).__init__(*args, **kwargs)

    code = forms.CharField(required=True, max_length=10, label='Код подтвержения',
                           widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                           error_messages={'required': 'Введите код!','max_length': 'Максимальное количество символов 10'})

    def save(self, commit=True):
        profile = super(ActivationCodeForm, self).save(commit=False)
        profile.code = self.cleaned_data['code']

        if commit:
            profile.save()
        return profile


