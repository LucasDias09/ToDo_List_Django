from django.db import models
from django.urls import reverse


class Tarefa(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    completa = models.BooleanField(default=False)
    data_vencimento = models.DateTimeField(blank=True, null=True)
    ordem = models.PositiveIntegerField(default=0, blank=False, null=False) 

    class Meta:
        # A nova ordenação padrão será pelo campo 'ordem'
        ordering = ['ordem', 'data_vencimento']
    

    def __str__(self):
        return self.titulo
    
    # URL para redirecionar após a criação ou edição
    def get_absolute_url(self):
        return reverse('task_detail', kwargs={'pk': self.pk}) 

class Rating(models.Model):
    tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
 


    def __str__(self):
        return f"Rating for {self.tarefa.titulo}: {self.rating}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        ordering = ['-sent_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
    
    
    
    def __str__(self):
        return f"Message from {self.name} <{self.email}>"
    def get_absolute_url(self):
        return reverse('contact_page')
    

    