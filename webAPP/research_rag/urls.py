from django.urls import path
from . import views

urlpatterns = [
    # Strona główna
    path('', views.index, name='index'),
    
    # Zapytania
    path('ask/', views.ask_question, name='ask_question'),
    path('history/', views.query_history, name='query_history'),
    
    # Konfiguracje
    path('config/', views.configurations, name='configurations'),
    path('config/new/', views.configuration_create, name='configuration_create'),
    path('config/<int:config_id>/edit/', views.configuration_edit, name='configuration_edit'),
    path('config/<int:config_id>/delete/', views.configuration_delete, name='configuration_delete'),
    path('config/<int:config_id>/activate/', views.activate_configuration, name='activate_configuration'),
    
    # Zarządzanie bazą danych
    path('database/', views.database_management, name='database_management'),
    
    # API endpoints
    path('api/test-model/', views.test_model, name='test_model'),
]
