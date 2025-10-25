from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import ContactMessage, Tarefa
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json





# 1. LIST (R)
class TaskListView(ListView):
    model = Tarefa 
    template_name = 'tasks/task_list.html' 
    context_object_name = 'tarefas' 
    

# 2. CREATE (C)
class TaskCreateView(CreateView):
    model = Tarefa 
    template_name = 'tasks/task_form.html'
    fields = ['titulo', 'descricao', 'completa']

# 3. DETAIL (R)
class TaskDetailView(DetailView):
    model = Tarefa
    template_name = 'tasks/task_detail.html'
    context_object_name = 'tarefa'

# 4. UPDATE (U)
class TaskUpdateView(UpdateView):
    model = Tarefa
    template_name = 'tasks/task_form.html'
    fields = ['titulo', 'descricao', 'completa']

# 5. DELETE (D)
class TaskDeleteView(DeleteView):
    model = Tarefa
    template_name = 'tasks/task_confirm_delete.html'
    context_object_name = 'tarefa'
    success_url = reverse_lazy('task_list') 

@method_decorator(csrf_exempt, name='dispatch') # Necessário para POST sem formulário
class TaskReorderView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            # data será uma lista de objetos: [{'id': 1, 'ordem': 0}, {'id': 2, 'ordem': 1}, ...]
            
            # Percorre a nova ordem e atualiza o BD
            for item in data:
                Tarefa.objects.filter(pk=item['id']).update(ordem=item['ordem'])
            
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

# Página de Contacto
class ContactPageView(CreateView):
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
class MessagePageView(ListView):
    template_name = 'tasks/messages.html'
    model = ContactMessage
    context_object_name = 'messages'    
    
    