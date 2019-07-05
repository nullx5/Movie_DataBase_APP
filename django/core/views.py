#from django.shortcuts import render

#Vistas basadas en clases ListView.
from django.views.generic import ListView

from core.models import Movie

class MovieList(ListView):
     model = Movie 

# Create your views here.
