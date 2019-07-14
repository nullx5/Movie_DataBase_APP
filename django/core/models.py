from django.db import models

# Create your models here.
"""
NOTA:
	Acceso a todos los registros ->  Movie.objects.all() | dir(Sleuth) all methods | dir(Movie.objects) | dir(Movie)
	Movie.NOT_RATED -> 0 |  test.rating -> 0-  mismo resultado
	atributo ordering de clase Meta  Equivale a ORDER BY year DESC, title;
	OJO: El orden de las clases importa.
"""
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
    #Relaciones
    director = models.ForeignKey(to='Person', on_delete = models.SET_NULL, related_name = 'directed', null = True, blank = True)
    writers = models.ManyToManyField(to = 'Person', related_name = 'writing_credits', blank = True)
    actors = models.ManyToManyField(to = 'Person', through = 'Role', related_name = 'acting_credits', blank = True) #Solo actors agrega nueva Clase Role ?
   
    class Meta:
        ordering = ('-year', 'title') 

    def __str__(self):
        return '{} ({})'.format(self.title, self.year)

class Person(models.Model):
    first_name = models.CharField(max_length=140)
    last_name = models.CharField(max_length=140)
    born = models.DateField()
    died = models.DateField(null="True", blank="True")

    class Meta:
        ordering = ("last_name", "first_name")

    def __str__(self):
        if self.died:
            return "{}, {} ({}-{})".format(self.last_name, self.first_name, self.born, self.died)

        return "{}, {} ({})".format(self.last_name, self.first_name, self.born) 


class Role(models.Model):
    movie = models.ForeignKey(Movie, on_delete = models.DO_NOTHING)
    person = models.ForeignKey(Person, on_delete = models.DO_NOTHING)
    name = models.CharField(max_length = 140)

    def __str__(self):
        return "{} {} {}".format(self.movie_id, self.person_id, self.name)

    class Meta:
        unique_together = ('movie', 'person', 'name')
