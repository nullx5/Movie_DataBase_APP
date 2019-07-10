#from django.shortcuts import render

#Vistas basadas en clases ListView.
from django.views.generic import ListView, DetailView

from core.models import Movie

class MovieList(ListView): #All models - work with object_list in the template
     model = Movie
 
class MovieDetail(DetailView): #Una instancia del modelo  a la vez
    model = Movie

# Create your views here.
