from  django.urls import path

from . import views

app_name = 'core' #App a la que pertenece el URLConf

urlpatterns = [
	path('movies', views.MovieList.as_view(), name = 'MovieList'), #Buena practica  nombrar las paths | Vistas basadas en Clases usan as_view().
	path('movie/<int:pk>', views.MovieDetail.as_view(), name = 'MovieDetail'), #MovieDetail espera que se le pase una pk o slug(URL-amigable) en la URL.
        path('person/<int:pk>', views.PersonDetail.as_view(), name = 'PersonDetail')
]
