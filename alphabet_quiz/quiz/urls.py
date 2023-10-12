from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add-data/', views.add_data_get, name='add_data_get'),
    path('add-data/', views.add_data_post, name='add_data_post'),
    path('practice/', views.practice_get, name='practice_get'),
    path('practice-post/', views.practice_post, name='practice_post'),  # POST request
    path('practice_numb/', views.practice_numb_get, name='practice_numb_get'),
    path('practice_numb-post/', views.practice_numb_post, name='practice_numb_post'),  # POST request
]
