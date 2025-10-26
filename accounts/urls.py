from django.urls import path
from django.contrib.auth import views as auth_views # Importa as views integradas do Django
from .views import SignUpView

urlpatterns = [
    # Login: Usa a View integrada LoginView
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    
    # Logout: Usa a View integrada LogoutView
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Registo: Usa a nossa view personalizada
    path('signup/', SignUpView.as_view(), name='signup'),
]
