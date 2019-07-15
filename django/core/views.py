#from django.shortcuts import render

#Vistas basadas en clases ListView.
from django.views.generic import ListView, DetailView
from core.models import Movie, Person

class MovieList(ListView): #All models - work with object_list in the template
     model = Movie
     paginate_by = 5

class MovieDetail(DetailView): #Una instancia del modelo  a la vez
    #model = Movie
    queryset = (Movie.objects.all_with_related_persons())
 
class PersonDetail(DetailView):
    queryset = Person.objects.all_with_prefetch_movies()

    


