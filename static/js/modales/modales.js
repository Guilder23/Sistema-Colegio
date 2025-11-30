// Funciones globales para abrir y cerrar modales
function abrirModal(modalId) {
    const modalElement = document.getElementById(modalId);
    if (modalElement) {
        const modal = new bootstrap.Modal(modalElement);
        modal.show();
    }
}

function cerrarModal(modalId) {
    const modalElement = document.getElementById(modalId);
    if (modalElement) {
        const modal = bootstrap.Modal.getInstance(modalElement);
        if (modal) {
            modal.hide();
        }
    }
}

// Clase Modal personalizada (para compatibilidad)
class Modal {
    constructor(modalId) {
        this.modalId = modalId;
        this.modal = document.getElementById(modalId);
        this.bsModal = null;
        if (this.modal) {
            this.bsModal = new bootstrap.Modal(this.modal);
        }
    }

    open() {
        if (this.bsModal) {
            this.bsModal.show();
        }
    }

    close() {
        if (this.bsModal) {
            this.bsModal.hide();
        }
    }

    toggle() {
        if (this.bsModal) {
            this.bsModal.toggle();
        }
    }
}

// Inicializar al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    const modalTriggers = document.querySelectorAll('[data-modal-trigger]');
    
    modalTriggers.forEach(trigger => {
        trigger.addEventListener('click', () => {
            const modalId = trigger.getAttribute('data-modal-trigger');
            abrirModal(modalId);
        });
    });
});
