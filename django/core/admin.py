from django.contrib import admin

#Agregando nuestro modelo Movie al ADMIN  de django, accesible desde el browser.
from core.models import Movie


# Register your models here.
admin.site.register(Movie)


