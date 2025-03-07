from django.urls import path
from . import views

app_name = 'submissions'

urlpatterns = [
        path('submit/', views.submit_api, name='submit_api'),
        path('results/<str:task_id>', views.results_api, name='results_api'),

]
