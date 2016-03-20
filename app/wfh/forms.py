from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="密码")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="确认")
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        labels = {
            'username': ('账号'),
            'email': ('邮箱'),
        }
