from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

# View para Registo de Novo Utilizador (Signup)
class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login') # Após o registo, redireciona para a página de login

# Nota: Não foi preciso definir views para Login e Logout, 
# foi usado as views Class-Based integradas do Django (auth.views).
