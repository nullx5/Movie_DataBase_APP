from django.db import models

# Create your models here.

class Movie(models.Model):
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
    
    class Meta:
        ordering = ('-year', 'title') # Equivale a ORDER BY year DESC, title

    def __str__(self):
        return '{} ({})'.format(self.title, self.year) #Access into shell Movie.objects.all() | dir(Sleuth) all methods | dir(Movie.objects) | dir(Movie)

							#Movie.NOT_RATED -> 0 |  test.rating -> 0 
 
#Use python Shell (python manage.py shell - python manage.py dbshell)to Add records to DB. 
'''
from core.models import Movie
sleuth =  Movie.objects.create(
    title="Sleuth",
    plot="An snobbish writer who loves games"
    " invites his wife\'s lover for a battle of wits.", 
    year="1972",
    runtime="138",
)

The_Italian_Job =  Movie.objects.create(
    title="The Italian Job",
    plot="A comic caper run by a cockney criminal"
    "centres on hinges on a trafic jam", 
    year="1969",
    runtime="99",
)
'''
