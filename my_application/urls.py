from django.urls import path
from . import views

urlpatterns = [
    path('my_application/', views.my_application, name='my_application'),
    path('my_application/templates/soccer_info.html', views.foo_1, name='foo_1'),
    path('my_application/templates/emblem_check.html', views.foo_2, name='foo_2'),
    path('my_application/templates/art_gallery.html', views.foo_3, name='foo_3'),
    path('my_application/templates/comentarii.html', views.comentarii, name='comentarii'),
    path('my_application/templates/inscrieri.html', views.inscrieri, name='inscrieri'),
    path('my_application/templates/meciuri.html', views.meciuri, name='meciuri'),
    path('my_application/templates/prelucrare.html', views.prelucrare, name='prelucrare'),
]
