#from django.shortcuts import render

#Vistas basadas en clases ListView.
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin #Asegura que el usuario ha iniciado sesión
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse

from core.forms import VoteForm, MovieImageForm
from core.models import Movie, Person, Vote

class MovieList(ListView): #All models - work with object_list in the template
     model = Movie
     paginate_by = 15

class MovieDetail(DetailView): #Una instancia del modelo  a la vez
   
    """get the user's vote for the movie, instantiate the form, and know which URL to
       ubmit the vote to (create_vote or update_vote).
    """
    queryset = (Movie.objects.all_with_related_persons_and_score())  # cumple misma funcion que model = Movie
    
    def get_context_data(self, **kwargs):# get_context_data Obtiene datos del contexto variables, objectos, etc, que le vas a pasar al template 
        ctx = super().get_context_data(**kwargs)
        ctx["image_form"] = self.movie_image_form()
        if self.request.user.is_authenticated:
            vote = Vote.objects.get_vote_or_unsaved_blank_vote(movie = self.object, user = self.request.user) #Obtiene movie y usuario
            if vote.id:
                vote_form_url = reverse('core:UpdateVote', kwargs = {'movie_id': vote.movie.id, "pk": vote.id})
            else:
                vote_form_url = (reverse("core:CreateVote", kwargs = {"movie_id":self.object.id}))
            vote_form = VoteForm(instance = vote)
            ctx["vote_form"] = vote_form
            ctx["vote_form_url"] = vote_form_url
        return ctx
    
    def movie_image_form(self):
        if self.request.user.is_authenticated:
            return MovieImageForm()
        return None

class PersonDetail(DetailView):
    queryset = Person.objects.all_with_prefetch_movies()

class CreateVote(LoginRequiredMixin, CreateView):
    form_class = VoteForm

    def get_initial(self):
        initial = super().get_initial()
        initial["user"] = self.request.user.id
        initial["movie"] = self.kwargs["movie_id"]
        return initial 

    def get_success_url(self):
        movie_id = self.object.movie.id
        return reverse("core:MovieDetail", kwargs={"pk": movie_id})

    def render_to_response(self, context, **response_kwargs):
        movie_id = context["object"].id
        movie_detail_url = reverse("core:MovieDetail", kwargs={"pk": movie_id})
        return redirect(to=movie_detail_url) #redireccion despues de votar
 

class UpdateVote(LoginRequiredMixin, UpdateView):
    form_class = VoteForm
    queryset = Vote.objects.all()

    def get_object(self, queryset=None):
        vote = super().get_object(queryset)
        user = self.request.user

        if vote.user != user:
            raise PermisionDenied("cannot change anoher", "users vote")
        return vote

    def get_success_url(self):
        movie_id = self.object.movie.id
        return reverse('core:MovieDetail', kwargs={'pk': movie_id})

    def render_to_response(self, context, **response_kwargs):
        movie_id = context['object'].id
        movie_datail_url = reverse('core:MovieDetail', kwargs={'pk': movie_id})
        return redirect(to=movie_detail_url)#redireccion despues de actualizar voto


class MovieImageUpload(LoginRequiredMixin, CreateView):

    """
    Nuestra vista una vez más delega todo el trabajo de validar y guardar 
    el modelo en CreateView y nuestro formulario.
    """
    form_class = MovieImageForm

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.id
        initial['movie'] = self.kwargs['movie_id']
        return initial

    def render_to_response(self, context, **response_kwargs):
        movie_id = self.kwargs['movie_id']
        movie_detail_url = reverse('core:MovieDetail', kwargs={'pk': movie_id})
        return redirect(to = movie_detail_url)

    def get_success_url(self):
        movie_id = self.kwargs['movie_id']
        movie_detail_url = reverse('core:MovieDetail', kwargs = {'pk': movie_id})
        return movie_detail_url

