/**
 * RAG Research Assistant - Main JavaScript
 * Handles application interactivity, AJAX requests and animations
 */

$(document).ready(function() {
    // Initialize application
    initializeApp();
    
    // Event listeners
    setupEventListeners();
    
    // Loading animations
    setupAnimations();
});

/**
 * Initialize main application functions
 */
function initializeApp() {
    // Hide loading overlay if exists
    hideLoadingOverlay();
    
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);
}

/**
 * Configure event listeners
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
    
    // Smooth scroll for links
    $('a[href^="#"]').on('click', handleSmoothScroll);
}

/**
 * Configure animations
 */
function setupAnimations() {
    // Fade in for cards
    $('.card').addClass('fade-in-up');
    
    // Staggered animation for list elements
    $('.list-group-item, .table tbody tr').each(function(index) {
        $(this).css('animation-delay', (index * 0.1) + 's');
        $(this).addClass('fade-in-up');
    });
}

/**
 * Handle query submission via AJAX
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
                showAlert('Error: ' + (data.error || 'Unknown error'), 'danger');
            }
        },
        error: function(xhr, status, error) {
            hideQueryLoading(submitBtn);
            showAlert('Connection error: ' + error, 'danger');
        }
    });
}

/**
 * Show loading state for query form
 */
function showQueryLoading(submitBtn) {
    submitBtn.prop('disabled', true);
    submitBtn.html('<i class="fas fa-spinner fa-spin me-2"></i>Analyzing...');
    
    // Show progress bar
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
                    <i class="fas fa-robot me-2"></i>AI Answer
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
                        ${new Date().toLocaleString('en-US')}
                    </div>
                    <div class="col-sm-6 text-sm-end">
                        <i class="fas fa-database me-1"></i>
                        Processing time: ${processingTime}s
                    </div>
                </div>
            </div>
        </div>
    `;
    
    container.html(responseHtml);
    
    // Smooth scroll to response
    $('html, body').animate({
        scrollTop: container.offset().top - 100
    }, 500);
}

/**
 * Format response text (markdown-like)
 */
function formatResponseText(text) {
    if (!text) return '';
    
    // Basic formatting
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>');
}

/**
 * Handle model testing
 */
function handleModelTest(e) {
    e.preventDefault();
    
    const btn = $(this);
    const originalText = btn.html();
    const modelName = $('#id_model_name').val();
    const ollamaUrl = $('#id_ollama_url').val();
    
    if (!modelName || !ollamaUrl) {
        showAlert('Please enter model name and Ollama URL.', 'warning');
        return;
    }
    
    // Loading state
    btn.prop('disabled', true);
    btn.html('<i class="fas fa-spinner fa-spin me-2"></i>Testing...');
    
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
            showAlert('Error during model testing.', 'danger');
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
    
    if (!confirm(`Are you sure you want to activate configuration "${configName}"?`)) {
        return;
    }
    
    const originalText = btn.html();
    btn.prop('disabled', true);
    btn.html('<i class="fas fa-spinner fa-spin me-2"></i>Activating...');
    
    $.ajax({
        url: `/config/${configId}/activate/`,
        type: 'POST',
        success: function(data) {
            if (data.success) {
                showAlert(data.message, 'success');
                // Refresh page after 1 second
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
 * Handle database preparation
 */
function handleDatabasePreparation(e) {
    const submitBtn = $(this).find('button[type="submit"]');
    const searchTopic = $(this).find('input[name="search_topic"]').val().trim();
    
    if (!searchTopic) {
        e.preventDefault();
        showAlert('Please enter a search topic.', 'warning');
        return;
    }
    
    // Show warning about duration
    if (!confirm('Database preparation may take several minutes. Continue?')) {
        e.preventDefault();
        return;
    }
    
    // Loading state
    submitBtn.prop('disabled', true);
    submitBtn.html('<i class="fas fa-spinner fa-spin me-2"></i>Preparing database...');
    
    // Form will be submitted normally (not AJAX)
}

/**
 * Auto-resize textarea
 */
function autoResizeTextarea() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
}

/**
 * Smooth scroll for links
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
 * Update recent queries list
 */
function updateRecentQueries() {
    // Can implement AJAX to refresh list
    // For now leave empty
}

/**
 * Show alert
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
    
    // Add alert to top of page
    $('.main-content .container').prepend(alertHtml);
    
    // Auto-hide after 5 seconds
    setTimeout(function() {
        $('.alert').first().fadeOut('slow', function() {
            $(this).remove();
        });
    }, 5000);
}

/**
 * Show loading overlay
 */
function showLoadingOverlay(message = 'Loading...') {
    const overlayHtml = `
        <div class="loading-overlay">
            <div class="loading-content">
                <div class="spinner-border spinner-border-purple mb-3" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <h5>${message}</h5>
            </div>
        </div>
    `;
    $('body').append(overlayHtml);
}

/**
 * Hide loading overlay
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
 * Utility: Format numbers
 */
function formatNumber(num) {
    return new Intl.NumberFormat('en-US').format(num);
}

/**
 * Utility: Format time
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
