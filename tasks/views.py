from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import ContactMessage, Tarefa
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
import json





# 1. LIST (R)
class TaskListView(LoginRequiredMixin,ListView):
    model = Tarefa 
    template_name = 'tasks/task_list.html' 
    context_object_name = 'tarefas' 

    # FILTRO: Sobrescreve get_queryset para filtrar as tarefas pelo utilizador logado
    def get_queryset(self):
        # Apenas retorna tarefas onde o campo 'user' é igual ao utilizador atual
        return Tarefa.objects.filter(user=self.request.user).order_by('ordem')
    

# 2. CREATE (C)
class TaskCreateView(LoginRequiredMixin,CreateView):
    model = Tarefa 
    template_name = 'tasks/task_form.html'
    fields = ['titulo', 'descricao', 'completa']
    # Adiciona automaticamente o utilizador e a ordem
    def form_valid(self, form):
        # 1. Atribui o utilizador antes de salvar o formulário
        form.instance.user = self.request.user
        
        # 2. Define a ordem (coloca a nova tarefa no final)
        latest_order = Tarefa.objects.filter(user=self.request.user).aggregate(models.Max('ordem'))['ordem__max']
        form.instance.ordem = (latest_order or 0) + 1
        
        return super().form_valid(form)

# 3. DETAIL (R)
class TaskDetailView(LoginRequiredMixin,DetailView):
    model = Tarefa
    template_name = 'tasks/task_detail.html'
    context_object_name = 'tarefa'
    # Garante que o utilizador só pode ver as suas próprias tarefas
    def get_queryset(self):
        return Tarefa.objects.filter(user=self.request.user)

# 4. UPDATE (U)
class TaskUpdateView(LoginRequiredMixin,UpdateView):
    model = Tarefa
    template_name = 'tasks/task_form.html'
    fields = ['titulo', 'descricao', 'completa']
    # Garante que o utilizador só pode editar as suas próprias tarefas
    def get_queryset(self):
        return Tarefa.objects.filter(user=self.request.user)

# 5. DELETE (D)
class TaskDeleteView(LoginRequiredMixin,DeleteView):
    model = Tarefa
    template_name = 'tasks/task_confirm_delete.html'
    context_object_name = 'tarefa'
    success_url = reverse_lazy('task_list') 
    # Garante que o utilizador só pode apagar as suas próprias tarefas
    def get_queryset(self):
        return Tarefa.objects.filter(user=self.request.user)

@method_decorator(csrf_exempt, name='dispatch') # Necessário para POST sem formulário
class TaskReorderView(View):
    # Lógica de reordenação (garantir que só mexe nas suas próprias tarefas)
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            
            for item in data:
                # Filtrar pelo ID E pelo Utilizador para segurança
                Tarefa.objects.filter(pk=item['id'], user=request.user).update(ordem=item['ordem'])
            
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

# Página de Contacto
class ContactPageView(LoginRequiredMixin,CreateView):
    template_name = 'tasks/contact_page.html'
    model = ContactMessage
    fields = ['name', 'email', 'message']
    success_url = reverse_lazy('contact_page')

    def get(self, request, *args, **kwargs):
        messages = self.model.objects.all()
        return render(request, self.template_name, {'messages': messages})

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        ContactMessage.objects.create(name=name, email=email, message=message)

        return render(request, self.template_name, {'success': True})

# Página de Mensagens
class MessagePageView(LoginRequiredMixin,ListView):
    template_name = 'tasks/messages.html'
    model = ContactMessage
    context_object_name = 'messages'    
    
    