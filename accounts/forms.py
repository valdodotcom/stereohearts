from django.forms import ModelForm
from .models import User
from django.forms import PasswordInput
from django.contrib.auth.hashers import make_password

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': PasswordInput(render_value=True),
        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user