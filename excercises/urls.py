from django.urls import path
from . import views

app_name = 'excercises'

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<slug:course_slug>/', views.course_details, name='course_details'),
    path('<slug:course_slug>/unit/create/', views.unit_create, name='unit_create'),
    path('<slug:course_slug>/unit/<int:unit_pk>/edit/', views.unit_edit, name='unit_edit'),
    path('<slug:course_slug>/activity/create/', views.excercise_create, name='excercise_create'),
    path('<slug:course_slug>/activity/<int:excercise_pk>/', views.excercise_details, name='excercise_details'),
    path('<slug:course_slug>/activity/<int:excercise_pk>/edit/', views.excercise_edit, name='excercise_edit')
]