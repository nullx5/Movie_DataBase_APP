#from django.shortcuts import render -> by default

from django.contrib.auth.forms import UserCreationForm #La aplicación de auth incorporada de Django, ya tiene un modelo de user que podemos usar.
from django.urls import reverse_lazy
from django.views.generic import CreateView

class RegisterView(CreateView):
    """
    Sí CreateView recibe una petición GET, eso renderizara el template para el formulario.
    Sí recibe una petición POST guardara los datos en la DB, si estos validos, si no enviara un mensaje de error
    """
    template_name = 'user/register.html' #usa variable form en el template
    form_class = UserCreationForm # los modelos simples son model = MyModel, Pero un user es más complejo, UserCreationForm se encarga del modelo por nosotros
    success_url = reverse_lazy('core:MovieList') # Cuando la creación del modelo tiene éxito, esta es la URL a la que debe redirigir


