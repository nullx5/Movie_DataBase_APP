from django.db import models #define the fields
from django.conf import settings #AUTH_USER_MODEL
from django.db.models.aggregates import Sum
# Create your models here.
"""
NOTA:
	Acceso a todos los registros ->  Movie.objects.all() | crear registros sleuth = Movie.objects.create() | dir(Sleuth) all methods | dir(Movie.objects) | dir(Movie)
	Movie.NOT_RATED -> 0 |  test.rating -> 0-  mismo resultado
	atributo ordering de clase Meta  Equivale a ORDER BY year DESC, title;
	OJO: El orden de las clases importa, clase <Role> de la relacion ManyToManyField Movie to Person va al final | NameError: name 
"""
class PersonManager(models.Manager):
    def all_with_prefetch_movies(self):
        qs = self.get_queryset()
        return qs.prefetch_related('directed', 'writing_credits', 'role_set__movie')

class Person(models.Model):
    first_name = models.CharField(max_length=140)
    last_name = models.CharField(max_length=140)
    born = models.DateField()
    died = models.DateField(null="True", blank="True")
    objects = PersonManager()

    class Meta:
        ordering = ("last_name", "first_name")

    def __str__(self):
        if self.died:
            return "{}, {} ({}-{})".format(self.last_name, self.first_name, self.born, self.died)

        return "{}, {} ({})".format(self.last_name, self.first_name, self.born)

class MovieManager(models.Manager):
    def all_with_related_persons(self):
        qs = self.get_queryset()
        qs = qs.select_related('director')
        qs = qs.prefetch_related('writers', 'actors')
        return qs
    
    def all_with_related_persons_and_score(self):
        """
             Django abstracts most common
                SQL aggregate functions, including Sum, Count and Average
        """
        qs = self.all_with_related_persons()
        qs = qs.annotate(score=Sum("vote__value"))
        return qs   

class Movie(models.Model):
    """
        Relaciones  Movie to Person
	ForeingKey - director | 
	ManyToManyField writers | 
	ManyToManyField actors - agrega nueva clase Role con ForeingKeys de Movie y Person clases
    """

    NOT_RATED = 0
    RATED_G = 1
    RATED_PG = 2
    RATED_R = 3
    RATINGS = (
        (NOT_RATED, 'NR - Not Rated'),
        (RATED_G,
	 'G - General Audiences'),
	(RATED_PG,
	 'PG - Parental guidance'
	'Suggested'),
	(RATED_R, 'R - Restricted'),
	)
    title = models.CharField(max_length=140)
    plot = models.TextField()
    year = models.PositiveIntegerField()
    rating = models.IntegerField(choices=RATINGS, default=NOT_RATED)
    runtime = models.PositiveIntegerField()
    website = models.URLField(blank=True)
    #Campos de Relaciones
    director = models.ForeignKey(to='Person', on_delete = models.SET_NULL, related_name = 'directed', null = True, blank = True)
    writers = models.ManyToManyField(to = 'Person', related_name = 'writing_credits', blank = True)
    actors = models.ManyToManyField(to = 'Person', through = 'Role', related_name = 'acting_credits', blank = True) #Solo actors agrega nueva Clase Role ?
    objects = MovieManager()

    class Meta:
        ordering = ('-year', 'title') 

    def __str__(self):
        return '{} ({})'.format(self.title, self.year)

class Role(models.Model):
    person = models.ForeignKey(Person, on_delete = models.DO_NOTHING)
    movie = models.ForeignKey(Movie, on_delete = models.DO_NOTHING)
    name = models.CharField(max_length = 140)

    def __str__(self):
        return "{} {} {}".format(self.movie_id, self.person_id, self.name)

    class Meta:
        unique_together = ('movie', 'person', 'name')

class VoteManager(models.Manager):
    """
     Comprueba si un modelo de user tiene una instancia de modelo de vote 
     relacionada para una instancia de modelo de película determinada
    """
    def get_vote_or_unsaved_blank_vote(self, movie, user):
        try:
             return Vote.objects.get(movie=movie, user=user)

        except Vote.DoesNotExist:

            return Vote(movie=movie, user=user) # El uso del constructor crea un nuevo modelo en la memoria pero no en la base de datos. A diferencia del método create () de su manager.

class Vote(models.Model):
    UP = 1
    DOWN = -1
    VALUE_CHOICES = ((UP, "👍"), (DOWN, "👎"))
    value = models.SmallIntegerField(choices = VALUE_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 	on_delete = models.CASCADE)# ?
    movie = models.ForeignKey(Movie, on_delete = models.CASCADE)
    vote_on = models.DateTimeField(auto_now =  True)
    
    objects = VoteManager()

    class Meta:
        unique_together = ("user", "movie")
