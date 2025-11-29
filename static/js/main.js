// ==================== MAIN.JS - FUNCIONALIDADES GLOBALES ====================

document.addEventListener('DOMContentLoaded', () => {
    // Navbar dropdown toggle
    const navbarUserBtn = document.querySelector('.navbar-user-btn');
    const navbarDropdown = document.querySelector('.navbar-dropdown');
    const navbarMobileToggle = document.querySelector('.navbar-mobile-toggle');
    const navbarMenu = document.querySelector('.navbar-menu');

    // Dropdown de usuario
    if (navbarUserBtn && navbarDropdown) {
        navbarUserBtn.addEventListener('click', () => {
            navbarDropdown.classList.toggle('show');
        });

        // Cerrar dropdown al hacer clic fuera
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.navbar-user')) {
                navbarDropdown.classList.remove('show');
            }
        });
    }

    // Mobile menu toggle
    if (navbarMobileToggle && navbarMenu) {
        navbarMobileToggle.addEventListener('click', () => {
            navbarMenu.classList.toggle('show');
        });

        // Cerrar menú al hacer clic en un enlace
        const navbarItems = navbarMenu.querySelectorAll('.navbar-item a');
        navbarItems.forEach(item => {
            item.addEventListener('click', () => {
                navbarMenu.classList.remove('show');
            });
        });
    }

    // Sidebar toggle en mobile
    const sidebarToggleBtn = document.querySelector('[data-sidebar-toggle]');
    const sidebar = document.querySelector('.sidebar');
    if (sidebarToggleBtn && sidebar) {
        sidebarToggleBtn.addEventListener('click', () => {
            sidebar.classList.toggle('show');
        });

        // Cerrar sidebar al hacer clic en un enlace
        const sidebarLinks = sidebar.querySelectorAll('.sidebar-link');
        sidebarLinks.forEach(link => {
            link.addEventListener('click', () => {
                sidebar.classList.remove('show');
            });
        });
    }

    // Establecer enlace activo en sidebar
    const currentPath = window.location.pathname;
    const sidebarLinks = document.querySelectorAll('.sidebar-link');
    sidebarLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // Alertas que desaparecen automáticamente
    const alerts = document.querySelectorAll('[data-dismiss-alert]');
    alerts.forEach(alert => {
        const dismissTime = parseInt(alert.getAttribute('data-dismiss-alert')) || 5000;
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.3s ease';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, dismissTime);
    });

    // Confirmar eliminación
    const formsDelete = document.querySelectorAll('[data-confirm-delete]');
    formsDelete.forEach(form => {
        form.addEventListener('submit', (e) => {
            const message = form.getAttribute('data-confirm-message') || '¿Está seguro de que desea eliminar este elemento?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // Mostrar mensaje de carga en formularios
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = 'Cargando...';
            }
        });
    });

    // Smooth scroll para anclas
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#' && document.querySelector(href)) {
                e.preventDefault();
                document.querySelector(href).scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});

/* Funciones útiles globales */

// Formatear fecha
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('es-ES', options);
}

// Mostrar notificación
function showNotification(message, type = 'info', duration = 3000) {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    alert.style.position = 'fixed';
    alert.style.top = '100px';
    alert.style.right = '20px';
    alert.style.zIndex = '9999';
    alert.style.maxWidth = '400px';
    
    document.body.appendChild(alert);
    
    setTimeout(() => {
        alert.style.opacity = '0';
        alert.style.transition = 'opacity 0.3s ease';
        setTimeout(() => alert.remove(), 300);
    }, duration);
}

// Validar formulario
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// API call helper
async function apiCall(url, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    };
    
    if (data && method !== 'GET') {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Obtener cookie CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
