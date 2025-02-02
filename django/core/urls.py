from  django.urls import path

from . import views

app_name = 'core' #App a la que pertenece el URLConf

urlpatterns = [
	path('movies', views.MovieList.as_view(), name = 'MovieList'), #Buena practica  nombrar las paths | Vistas basadas en Clases usan as_view().
	path('movie/<int:pk>', views.MovieDetail.as_view(), name = 'MovieDetail'), #MovieDetail espera que se le pase una pk o slug(URL-amigable) en la URL.
        path('movie/<int:movie_id>/vote', views.CreateVote.as_view(), name='CreateVote'),
        path('movie/<int:movie_id>/vote/<int:pk>', views.UpdateVote.as_view(), name='UpdateVote'),
        path('person/<int:pk>', views.PersonDetail.as_view(), name = 'PersonDetail'),
        path('movie/<int:movie_id>/image/upload', views.MovieImageUpload.as_view(), name ='MovieImageUpload')
]
