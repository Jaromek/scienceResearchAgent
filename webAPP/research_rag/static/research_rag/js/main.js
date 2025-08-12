/**
 * RAG Research Assistant - Main JavaScript
 * Obsługuje interaktywność aplikacji, AJAX requests i animacje
 */

$(document).ready(function() {
    // Inicjalizacja aplikacji
    initializeApp();
    
    // Event listeners
    setupEventListeners();
    
    // Animacje przy ładowaniu
    setupAnimations();
});

/**
 * Inicjalizacja głównych funkcji aplikacji
 */
function initializeApp() {
    // Ukryj loading overlay jeśli istnieje
    hideLoadingOverlay();
    
    // Inicjalizuj tooltips Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Auto-hide alerts po 5 sekundach
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);
}

/**
 * Konfiguracja event listenerów
 */
function setupEventListeners() {
    // Query form AJAX
    $('#query-form').on('submit', handleQuerySubmission);
    
    // Model test
    $(document).on('click', '.test-model-btn', handleModelTest);
    
    // Configuration activation
    $(document).on('click', '.activate-config-btn', handleConfigActivation);
    
    // Database preparation
    $('#database-form').on('submit', handleDatabasePreparation);
    
    // Auto-resize textarea
    $('textarea').on('input', autoResizeTextarea);
    
    // Smooth scroll dla linków
    $('a[href^="#"]').on('click', handleSmoothScroll);
}

/**
 * Konfiguracja animacji
 */
function setupAnimations() {
    // Fade in dla kart
    $('.card').addClass('fade-in-up');
    
    // Staggered animation dla elementów listy
    $('.list-group-item, .table tbody tr').each(function(index) {
        $(this).css('animation-delay', (index * 0.1) + 's');
        $(this).addClass('fade-in-up');
    });
}

/**
 * Obsługa wysyłania zapytania przez AJAX
 */
function handleQuerySubmission(e) {
    e.preventDefault();
    
    const form = $(this);
    const formData = new FormData(form[0]);
    const submitBtn = form.find('button[type="submit"]');
    const responseContainer = $('#response-container');
    const query = form.find('textarea[name="query"]').val().trim();
    
    if (!query) {
        showAlert('Please enter a question.', 'warning');
        return;
    }
    
    // Show loading state
    showQueryLoading(submitBtn);
    responseContainer.empty();
    
    $.ajax({
        url: form.attr('action'),
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        },
        success: function(data) {
            hideQueryLoading(submitBtn);
            
            if (data.success) {
                showQueryResponse(data, responseContainer);
                form[0].reset();
                updateRecentQueries();
            } else {
                showAlert('Błąd: ' + (data.error || 'Nieznany błąd'), 'danger');
            }
        },
        error: function(xhr, status, error) {
            hideQueryLoading(submitBtn);
            showAlert('Błąd połączenia: ' + error, 'danger');
        }
    });
}

/**
 * Pokazuje loading state dla formularza zapytania
 */
function showQueryLoading(submitBtn) {
    submitBtn.prop('disabled', true);
    submitBtn.html('<i class="fas fa-spinner fa-spin me-2"></i>Analizuję...');
    
    // Pokaż progress bar
    const progressHtml = `
        <div id="query-progress" class="mt-3">
            <div class="card">
                <div class="card-body text-center">
                    <div class="spinner-border spinner-border-purple mb-3" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <h5>Analyzing question...</h5>
                    <p class="text-muted mb-0">Searching for relevant articles and generating response</p>
                </div>
            </div>
        </div>
    `;
    $('#response-container').html(progressHtml);
}

/**
 * Hide loading state for query form
 */
function hideQueryLoading(submitBtn) {
    submitBtn.prop('disabled', false);
    submitBtn.html('<i class="fas fa-search me-2"></i>Ask question');
    $('#query-progress').remove();
}

/**
 * Display query response
 */
function showQueryResponse(data, container) {
    const processingTime = data.processing_time ? (data.processing_time).toFixed(2) : 'N/A';
    
    const responseHtml = `
        <div class="query-response fade-in-up">
            <div class="d-flex justify-content-between align-items-start mb-3">
                <h4 class="text-purple mb-0">
                    <i class="fas fa-robot me-2"></i>Odpowiedź AI
                </h4>
                <span class="badge badge-purple">
                    <i class="fas fa-clock me-1"></i>${processingTime}s
                </span>
            </div>
            <div class="response-content">
                ${formatResponseText(data.answer)}
            </div>
            <div class="response-meta">
                <div class="row">
                    <div class="col-sm-6">
                        <i class="fas fa-calendar me-1"></i>
                        ${new Date().toLocaleString('pl-PL')}
                    </div>
                    <div class="col-sm-6 text-sm-end">
                        <i class="fas fa-database me-1"></i>
                        Czas przetwarzania: ${processingTime}s
                    </div>
                </div>
            </div>
        </div>
    `;
    
    container.html(responseHtml);
    
    // Smooth scroll do odpowiedzi
    $('html, body').animate({
        scrollTop: container.offset().top - 100
    }, 500);
}

/**
 * Formatuje tekst odpowiedzi (markdown-like)
 */
function formatResponseText(text) {
    if (!text) return '';
    
    // Podstawowe formatowanie
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>');
}

/**
 * Obsługa testowania modelu
 */
function handleModelTest(e) {
    e.preventDefault();
    
    const btn = $(this);
    const originalText = btn.html();
    const modelName = $('#id_model_name').val();
    const ollamaUrl = $('#id_ollama_url').val();
    
    if (!modelName || !ollamaUrl) {
        showAlert('Proszę wprowadzić nazwę modelu i URL Ollama.', 'warning');
        return;
    }
    
    // Loading state
    btn.prop('disabled', true);
    btn.html('<i class="fas fa-spinner fa-spin me-2"></i>Testuję...');
    
    $.ajax({
        url: '/api/test-model/',
        type: 'POST',
        data: JSON.stringify({
            model_name: modelName,
            ollama_url: ollamaUrl
        }),
        contentType: 'application/json',
        success: function(data) {
            btn.prop('disabled', false);
            btn.html(originalText);
            
            if (data.success) {
                showAlert(data.message, 'success');
            } else {
                showAlert(data.message, 'danger');
            }
        },
        error: function() {
            btn.prop('disabled', false);
            btn.html(originalText);
            showAlert('Błąd podczas testowania modelu.', 'danger');
        }
    });
}

/**
 * Handle configuration activation
 */
function handleConfigActivation(e) {
    e.preventDefault();
    
    const btn = $(this);
    const configId = btn.data('config-id');
    const configName = btn.data('config-name');
    
    if (!confirm(`Czy na pewno chcesz aktywować konfigurację "${configName}"?`)) {
        return;
    }
    
    const originalText = btn.html();
    btn.prop('disabled', true);
    btn.html('<i class="fas fa-spinner fa-spin me-2"></i>Aktywuję...');
    
    $.ajax({
        url: `/config/${configId}/activate/`,
        type: 'POST',
        success: function(data) {
            if (data.success) {
                showAlert(data.message, 'success');
                // Odśwież stronę po 1 sekundzie
                setTimeout(() => location.reload(), 1000);
            } else {
                showAlert(data.message, 'danger');
                btn.prop('disabled', false);
                btn.html(originalText);
            }
        },
        error: function() {
            showAlert('Error during configuration activation.', 'danger');
            btn.prop('disabled', false);
            btn.html(originalText);
        }
    });
}

/**
 * Obsługa przygotowania bazy danych
 */
function handleDatabasePreparation(e) {
    const submitBtn = $(this).find('button[type="submit"]');
    const searchTopic = $(this).find('input[name="search_topic"]').val().trim();
    
    if (!searchTopic) {
        e.preventDefault();
        showAlert('Proszę wprowadzić temat wyszukiwania.', 'warning');
        return;
    }
    
    // Pokaż warning o czasie trwania
    if (!confirm('Przygotowanie bazy danych może zająć kilka minut. Czy kontynuować?')) {
        e.preventDefault();
        return;
    }
    
    // Loading state
    submitBtn.prop('disabled', true);
    submitBtn.html('<i class="fas fa-spinner fa-spin me-2"></i>Przygotowuję bazę...');
    
    // Form zostanie wysłany normalnie (nie AJAX)
}

/**
 * Auto-resize textarea
 */
function autoResizeTextarea() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
}

/**
 * Smooth scroll dla linków
 */
function handleSmoothScroll(e) {
    const target = $(this.getAttribute('href'));
    if (target.length) {
        e.preventDefault();
        $('html, body').animate({
            scrollTop: target.offset().top - 80
        }, 500);
    }
}

/**
 * Aktualizuje listę ostatnich zapytań
 */
function updateRecentQueries() {
    // Można zaimplementować AJAX do odświeżenia listy
    // Na razie pozostawiamy puste
}

/**
 * Pokazuje alert
 */
function showAlert(message, type = 'info') {
    const alertClass = `alert-${type}`;
    const iconClass = {
        'success': 'fas fa-check-circle',
        'warning': 'fas fa-exclamation-triangle',
        'danger': 'fas fa-exclamation-circle',
        'info': 'fas fa-info-circle'
    }[type] || 'fas fa-info-circle';
    
    const alertHtml = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            <i class="${iconClass} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    // Dodaj alert na górę strony
    $('.main-content .container').prepend(alertHtml);
    
    // Auto-hide po 5 sekundach
    setTimeout(function() {
        $('.alert').first().fadeOut('slow', function() {
            $(this).remove();
        });
    }, 5000);
}

/**
 * Pokazuje loading overlay
 */
function showLoadingOverlay(message = 'Ładowanie...') {
    const overlayHtml = `
        <div class="loading-overlay">
            <div class="loading-content">
                <div class="spinner-border spinner-border-purple mb-3" role="status">
                    <span class="visually-hidden">Ładowanie...</span>
                </div>
                <h5>${message}</h5>
            </div>
        </div>
    `;
    $('body').append(overlayHtml);
}

/**
 * Ukrywa loading overlay
 */
function hideLoadingOverlay() {
    $('.loading-overlay').fadeOut('fast', function() {
        $(this).remove();
    });
}

/**
 * Utility: Debounce function
 */
function debounce(func, wait, immediate) {
    var timeout;
    return function() {
        var context = this, args = arguments;
        var later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        var callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

/**
 * Utility: Format liczb
 */
function formatNumber(num) {
    return new Intl.NumberFormat('pl-PL').format(num);
}

/**
 * Utility: Format czasu
 */
function formatDuration(seconds) {
    if (seconds < 60) {
        return `${seconds.toFixed(1)}s`;
    } else if (seconds < 3600) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = Math.floor(seconds % 60);
        return `${minutes}m ${remainingSeconds}s`;
    } else {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        return `${hours}h ${minutes}m`;
    }
}
