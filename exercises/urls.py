from django.urls import path
from . import views

app_name = 'exercises'

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<slug:course_slug>/', views.course_details, name='course_details'),
    path('<slug:course_slug>/unit/create/', views.unit_create, name='unit_create'),
    path('<slug:course_slug>/unit/<int:unit_pk>/edit/', views.unit_edit, name='unit_edit'),
    path('<slug:course_slug>/activity/create/', views.exercise_create, name='exercise_create'),
    path('<slug:course_slug>/activity/<int:exercise_pk>/', views.exercise_details, name='exercise_details'),
    path('<slug:course_slug>/activity/<int:exercise_pk>/edit/', views.exercise_edit, name='exercise_edit')
]