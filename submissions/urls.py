from django.urls import path
from . import views

app_name = 'submissions'

urlpatterns = [
        path('', views.index, name='index'),
        path('server_submit/', views.submit, name='submit'),
        path('submit/', views.submit_api, name='submit_api'),
        path('auto-submit/<int:num>', views.auto_submit, name='auto_submit'),
        path('results/<str:task_id>', views.results_api, name='results_api'),

]
