from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q
import json
import time

from .models import RAGConfiguration, QueryHistory, DatabasePreparationLog
from .forms import RAGConfigurationForm, QueryForm, DatabasePreparationForm, ModelTestForm
from .services import RAGService, DatabaseService, ConfigurationService


def index(request):
    """
    Strona główna aplikacji - interfejs do zadawania pytań.
    Wyświetla formularz zapytania i historię ostatnich pytań.
    """
    query_form = QueryForm()
    active_config = RAGConfiguration.get_active_config()
    
    # Pobierz ostatnie zapytania
    recent_queries = QueryHistory.objects.select_related('config_used').order_by('-created_at')[:5]
    
    context = {
        'query_form': query_form,
        'active_config': active_config,
        'recent_queries': recent_queries,
        'page_title': 'RAG Research Assistant'
    }
    
    return render(request, 'research_rag/index.html', context)


def ask_question(request):
    """
    Endpoint do przetwarzania zapytań użytkownika.
    Obsługuje AJAX requests i zwraca odpowiedzi w formacie JSON.
    """
    if request.method == 'POST':
        form = QueryForm(request.POST)
        
        if form.is_valid():
            query = form.cleaned_data['query']
            
            # Pobierz informacje o użytkowniku
            user_ip = request.META.get('REMOTE_ADDR')
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            
            # Inicjalizuj serwis RAG
            rag_service = RAGService()
            
            # Generuj odpowiedź
            result = rag_service.generate_answer(query, user_ip, user_agent)
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # AJAX request - zwróć JSON
                return JsonResponse(result)
            else:
                # Regular request - redirect with message
                if result['success']:
                    messages.success(request, 'Response generated successfully!')
                else:
                    messages.error(request, f"Error: {result['error']}")
                
                return redirect('index')
        
        # Invalid form
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'error': 'Invalid form data'
            })
        else:
            messages.error(request, 'Please enter a valid question.')
            return redirect('index')
    
    return redirect('index')


def configurations(request):
    """
    Strona zarządzania konfiguracjami RAG.
    Wyświetla listę konfiguracji i formularz dodawania nowej.
    """
    configs = RAGConfiguration.objects.all().order_by('-updated_at')
    
    context = {
        'configurations': configs,
        'page_title': 'Konfiguracje RAG'
    }
    
    return render(request, 'research_rag/configurations.html', context)


def configuration_create(request):
    """
    Tworzenie nowej konfiguracji RAG.
    """
    if request.method == 'POST':
        form = RAGConfigurationForm(request.POST)
        
        if form.is_valid():
            # Configuration validation
            validation_result = ConfigurationService.validate_configuration(form.cleaned_data)
            
            if validation_result['valid']:
                config = form.save()
                messages.success(request, f'Configuration "{config.name}" created successfully!')
                
                # Add warnings if any
                for warning in validation_result['warnings']:
                    messages.warning(request, warning)
                
                return redirect('configurations')
            else:
                for error in validation_result['errors']:
                    messages.error(request, error)
        else:
            messages.error(request, 'Please correct form errors.')
    else:
        form = RAGConfigurationForm()
    
    # Pobierz dostępne modele
    available_models = ConfigurationService.get_available_models()
    
    context = {
        'form': form,
        'available_models': available_models,
        'page_title': 'New RAG Configuration'
    }
    
    return render(request, 'research_rag/configuration_form.html', context)


def configuration_edit(request, config_id):
    """
    Edycja istniejącej konfiguracji RAG.
    """
    config = get_object_or_404(RAGConfiguration, id=config_id)
    
    if request.method == 'POST':
        form = RAGConfigurationForm(request.POST, instance=config)
        
        if form.is_valid():
            # Configuration validation
            validation_result = ConfigurationService.validate_configuration(form.cleaned_data)
            
            if validation_result['valid']:
                config = form.save()
                messages.success(request, f'Configuration "{config.name}" updated successfully!')
                
                # Add warnings if any
                for warning in validation_result['warnings']:
                    messages.warning(request, warning)
                
                return redirect('configurations')
            else:
                for error in validation_result['errors']:
                    messages.error(request, error)
        else:
            messages.error(request, 'Please correct form errors.')
    else:
        form = RAGConfigurationForm(instance=config)
    
    # Pobierz dostępne modele
    available_models = ConfigurationService.get_available_models()
    
    context = {
        'form': form,
        'config': config,
        'available_models': available_models,
        'page_title': f'Edit Configuration: {config.name}'
    }
    
    return render(request, 'research_rag/configuration_form.html', context)


def configuration_delete(request, config_id):
    """
    Usuwanie konfiguracji RAG.
    """
    config = get_object_or_404(RAGConfiguration, id=config_id)
    
    if request.method == 'POST':
        name = config.name
        config.delete()
        messages.success(request, f'Configuration "{name}" deleted successfully.')
        return redirect('configurations')
    
    context = {
        'config': config,
        'page_title': f'Delete Configuration: {config.name}'
    }
    
    return render(request, 'research_rag/configuration_confirm_delete.html', context)


def database_management(request):
    """
    Strona zarządzania bazą danych artykułów naukowych.
    """
    if request.method == 'POST':
        form = DatabasePreparationForm(request.POST)
        
        if form.is_valid():
            search_topic = form.cleaned_data['search_topic']
            custom_max_papers = form.cleaned_data.get('custom_max_papers')
            
            # Inicjalizuj serwis bazy danych
            db_service = DatabaseService()
            
            try:
                # Rozpocznij przygotowanie bazy danych w tle
                log_entry = db_service.prepare_database(search_topic, custom_max_papers)
                
                messages.success(request, f'Rozpoczęto przygotowanie bazy danych dla tematu: "{search_topic}"')
                return redirect('database_management')
                
            except Exception as e:
                messages.error(request, f'Error during database preparation: {str(e)}')
        else:
            messages.error(request, 'Please correct form errors.')
    else:
        form = DatabasePreparationForm()
    
    # Pobierz logi przygotowania bazy danych
    logs = DatabasePreparationLog.objects.select_related('config_used').order_by('-started_at')[:20]
    
    context = {
        'form': form,
        'logs': logs,
        'page_title': 'Zarządzanie bazą danych'
    }
    
    return render(request, 'research_rag/database_management.html', context)


def query_history(request):
    """
    Strona historii zapytań użytkowników.
    """
    # Wyszukiwanie
    search_query = request.GET.get('search', '')
    queryset = QueryHistory.objects.select_related('config_used').order_by('-created_at')
    
    if search_query:
        queryset = queryset.filter(
            Q(query_text__icontains=search_query) | 
            Q(response_text__icontains=search_query)
        )
    
    # Paginacja
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    queries = paginator.get_page(page_number)
    
    context = {
        'queries': queries,
        'search_query': search_query,
        'page_title': 'Historia zapytań'
    }
    
    return render(request, 'research_rag/query_history.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def test_model(request):
    """
    AJAX endpoint do testowania dostępności modelu Ollama.
    """
    try:
        data = json.loads(request.body)
        model_name = data.get('model_name')
        ollama_url = data.get('ollama_url')
        
        if not model_name or not ollama_url:
            return JsonResponse({
                'success': False,
                'message': 'Brak wymaganych parametrów'
            })
        
        # Utworz tymczasową konfigurację do testowania
        from .models import RAGConfiguration
        temp_config = RAGConfiguration(
            model_name=model_name,
            ollama_url=ollama_url
        )
        
        # Testuj model
        rag_service = RAGService(temp_config)
        result = rag_service.test_model_availability()
        
        return JsonResponse({
            'success': result['available'],
            'message': result['message']
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error during testing: {str(e)}'
        })


@csrf_exempt
@require_http_methods(["POST"])
def activate_configuration(request, config_id):
    """
    AJAX endpoint for configuration activation.
    """
    try:
        config = get_object_or_404(RAGConfiguration, id=config_id)
        
        # Deactivate all others
        RAGConfiguration.objects.filter(is_active=True).update(is_active=False)
        
        # Activate selected
        config.is_active = True
        config.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Configuration "{config.name}" activated successfully.'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error during activation: {str(e)}'
        })
