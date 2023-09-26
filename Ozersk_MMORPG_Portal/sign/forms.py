from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


#форма активации
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

    code = forms.CharField(required=True, max_length=50, label='Код подтвержения',
                           widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                           error_messages={'required': 'Введите код!','max_length': 'Максимальное количество символов 10'})

    def save(self, commit=True):
        profile = super(ActivationCodeForm, self).save(commit=False)
        profile.code = self.cleaned_data['code']

        if commit:
            profile.save()
        return profile


#Форма регистрации
class RegistrationForm(UserCreationForm):
    error_css_class = 'has-error'
    error_messages = {
                      'username_exists':
                          ("Пользователь уже существует"), }
    email = forms.EmailField(required=True, label='Email')
    username = forms.CharField(required=True, max_length=15, label='Логин',  min_length=2)
    password1 = forms.CharField(required=True, max_length=30, label='Пароль', min_length=8)
    password2 = forms.CharField(required=True, max_length=30, label='Повторите пароль')
    firstname = forms.CharField(required=True, max_length=25, label='Имя', )

    class Meta:
        model = User
        fields = (
            'username',
            'firstname',
            'email',
            'password1',
            'password2'
       )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            User._default_manager.get(username=username)
            # if the user exists, then let's raise an error message
            raise forms.ValidationError(
                self.error_messages['username_exists'],  # my error message
                code='username_exists',  # set the error message key
            )
        except User.DoesNotExist:
            return username  # if user does not exist so we can continue the registration process

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['firstname']
        user.password1 = self.cleaned_data['password1']
        user.password2 = self.cleaned_data['password2']
        user.is_active = False

        if commit:
            user.save()
        return user