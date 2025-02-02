from django.contrib.auth import views as auth_views # auth tambien proporciona log in/out se encarga de las vistas por nosotros
from django.urls import path
from user import views


app_name = "user"

urlpatterns = [
    path('register', views.RegisterView.as_view(), name = 'register'),
    path('login', auth_views.LoginView.as_view(), name = 'login'),
    path('logout', auth_views.LogoutView.as_view(), name = 'logout')


]
