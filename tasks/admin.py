from django.contrib import admin

# Register your models here.
from .models import Tarefa, Rating, ContactMessage


admin.site.register(Tarefa)
admin.site.register(Rating)
admin.site.register(ContactMessage)
