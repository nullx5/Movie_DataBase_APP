from  django.urls import path

from . import views

app_name = 'core' #App a la que pertenece el URLConf
urlpatterns = [
	path('movies', views.MovieList.as_view(), name = 'MovieList'), #Buena nonbrar laas paths.
]
