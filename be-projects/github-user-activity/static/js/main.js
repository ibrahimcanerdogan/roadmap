// Main JavaScript file for GitHub User Activity App

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functionality
    initializeApp();
});

function initializeApp() {
    // Auto-hide flash messages after 5 seconds
    autoHideFlashMessages();
    
    // Add smooth scrolling for anchor links
    addSmoothScrolling();
    
    // Add loading states to forms
    addFormLoadingStates();
    
    // Add keyboard shortcuts
    addKeyboardShortcuts();
    
    // Add intersection observer for animations
    addScrollAnimations();
    
    // Add copy functionality for usernames
    addCopyFunctionality();
}

// Auto-hide flash messages
function autoHideFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach(message => {
        setTimeout(() => {
            if (message && message.parentElement) {
                message.style.opacity = '0';
                message.style.transform = 'translateX(100%)';
                setTimeout(() => {
                    if (message.parentElement) {
                        message.remove();
                    }
                }, 300);
            }
        }, 5000);
    });
}

// Add smooth scrolling
function addSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Add loading states to forms
function addFormLoadingStates() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitButton = this.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.classList.add('loading');
                
                // Re-enable after a delay (in case of errors)
                setTimeout(() => {
                    submitButton.disabled = false;
                    submitButton.classList.remove('loading');
                }, 10000);
            }
        });
    });
}

// Add keyboard shortcuts
function addKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K to focus search input
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.getElementById('username');
            if (searchInput) {
                searchInput.focus();
                searchInput.select();
            }
        }
        
        // Escape to clear search input
        if (e.key === 'Escape') {
            const searchInput = document.getElementById('username');
            if (searchInput && document.activeElement === searchInput) {
                searchInput.blur();
            }
        }
        
        // Enter to submit form when search input is focused
        if (e.key === 'Enter') {
            const searchInput = document.getElementById('username');
            if (searchInput && document.activeElement === searchInput && searchInput.value.trim()) {
                const form = searchInput.closest('form');
                if (form) {
                    form.submit();
                }
            }
        }
    });
}

// Add scroll animations
function addScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    const animateElements = document.querySelectorAll('.feature-card, .timeline-item, .stat-card');
    animateElements.forEach(el => {
        observer.observe(el);
    });
}

// Add copy functionality
function addCopyFunctionality() {
    const usernames = document.querySelectorAll('.user-name, .repo-name');
    
    usernames.forEach(username => {
        username.style.cursor = 'pointer';
        username.title = 'Click to copy';
        
        username.addEventListener('click', function() {
            const text = this.textContent;
            navigator.clipboard.writeText(text).then(() => {
                showCopyNotification(text);
            }).catch(() => {
                // Fallback for older browsers
                copyToClipboardFallback(text);
            });
        });
    });
}

// Show copy notification
function showCopyNotification(text) {
    const notification = document.createElement('div');
    notification.className = 'copy-notification';
    notification.textContent = `Copied "${text}" to clipboard!`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #28a745;
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 10000;
        font-size: 14px;
        font-weight: 500;
        transform: translateX(100%);
        transition: transform 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 300);
    }, 3000);
}

// Fallback copy function
function copyToClipboardFallback(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        showCopyNotification(text);
    } catch (err) {
        console.error('Failed to copy text: ', err);
    }
    
    document.body.removeChild(textArea);
}

// Utility function to debounce
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Add search suggestions functionality
function addSearchSuggestions() {
    const searchInput = document.getElementById('username');
    if (!searchInput) return;
    
    const suggestions = [
        'torvalds', 'gvanrossum', 'antirez', 'kamranahmedse',
        'tj', 'sindresorhus', 'addy-dclxvi', 'jashkenas',
        'defunkt', 'mojombo', 'pjhyett', 'wycats'
    ];
    
    let suggestionBox = null;
    
    searchInput.addEventListener('input', debounce(function() {
        const value = this.value.toLowerCase();
        
        if (suggestionBox) {
            suggestionBox.remove();
            suggestionBox = null;
        }
        
        if (value.length < 2) return;
        
        const matches = suggestions.filter(suggestion => 
            suggestion.toLowerCase().includes(value)
        );
        
        if (matches.length > 0) {
            suggestionBox = createSuggestionBox(matches, this);
            this.parentElement.appendChild(suggestionBox);
        }
    }, 300));
    
    // Close suggestions when clicking outside
    document.addEventListener('click', function(e) {
        if (suggestionBox && !suggestionBox.contains(e.target) && e.target !== searchInput) {
            suggestionBox.remove();
            suggestionBox = null;
        }
    });
}

// Create suggestion box
function createSuggestionBox(suggestions, input) {
    const box = document.createElement('div');
    box.className = 'suggestion-box';
    box.style.cssText = `
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: white;
        border: 1px solid #e1e4e8;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1000;
        max-height: 200px;
        overflow-y: auto;
    `;
    
    suggestions.forEach(suggestion => {
        const item = document.createElement('div');
        item.className = 'suggestion-item';
        item.textContent = suggestion;
        item.style.cssText = `
            padding: 12px 16px;
            cursor: pointer;
            border-bottom: 1px solid #f1f3f4;
            transition: background-color 0.15s ease;
        `;
        
        item.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#f6f8fa';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.backgroundColor = 'transparent';
        });
        
        item.addEventListener('click', function() {
            input.value = suggestion;
            input.focus();
            box.remove();
        });
        
        box.appendChild(item);
    });
    
    return box;
}

// Add error handling for failed API requests
function handleApiError(error) {
    console.error('API Error:', error);
    
    // Show user-friendly error message
    const errorMessage = document.createElement('div');
    errorMessage.className = 'flash-message flash-error';
    errorMessage.innerHTML = `
        <span class="flash-icon">❌</span>
        <span class="flash-text">Failed to load data. Please try again later.</span>
        <button class="flash-close" onclick="this.parentElement.remove()">×</button>
    `;
    
    const flashContainer = document.querySelector('.flash-messages') || createFlashContainer();
    flashContainer.appendChild(errorMessage);
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        if (errorMessage.parentElement) {
            errorMessage.remove();
        }
    }, 5000);
}

// Create flash container if it doesn't exist
function createFlashContainer() {
    const container = document.createElement('div');
    container.className = 'flash-messages';
    document.body.appendChild(container);
    return container;
}

// Add performance monitoring
function addPerformanceMonitoring() {
    // Monitor page load time
    window.addEventListener('load', function() {
        const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
        console.log(`Page loaded in ${loadTime}ms`);
        
        // Send to analytics if needed
        if (loadTime > 3000) {
            console.warn('Slow page load detected');
        }
    });
    
    // Monitor API response times
    const originalFetch = window.fetch;
    window.fetch = function(...args) {
        const start = performance.now();
        return originalFetch.apply(this, args).then(response => {
            const duration = performance.now() - start;
            console.log(`API request took ${duration.toFixed(2)}ms`);
            return response;
        });
    };
}

// Initialize additional features
document.addEventListener('DOMContentLoaded', function() {
    addSearchSuggestions();
    addPerformanceMonitoring();
});

// Export functions for global access
window.GitHubActivityApp = {
    copyToClipboard: function(text) {
        navigator.clipboard.writeText(text).then(() => {
            showCopyNotification(text);
        }).catch(() => {
            copyToClipboardFallback(text);
        });
    },
    
    showNotification: function(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `flash-message flash-${type}`;
        notification.innerHTML = `
            <span class="flash-icon">${type === 'error' ? '❌' : type === 'success' ? '✅' : 'ℹ️'}</span>
            <span class="flash-text">${message}</span>
            <button class="flash-close" onclick="this.parentElement.remove()">×</button>
        `;
        
        const flashContainer = document.querySelector('.flash-messages') || createFlashContainer();
        flashContainer.appendChild(notification);
        
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 5000);
    }
}; 