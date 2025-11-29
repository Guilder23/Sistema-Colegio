class Modal {
    constructor(modalId) {
        this.modal = document.getElementById(modalId);
        this.closeButtons = this.modal.querySelectorAll('[data-modal-close]');
        this.init();
    }

    init() {
        this.closeButtons.forEach(btn => {
            btn.addEventListener('click', () => this.close());
        });

        window.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.close();
            }
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.modal.classList.contains('show')) {
                this.close();
            }
        });
    }

    open() {
        this.modal.classList.add('show');
        document.body.style.overflow = 'hidden';
    }

    close() {
        this.modal.classList.remove('show');
        document.body.style.overflow = 'auto';
    }

    toggle() {
        if (this.modal.classList.contains('show')) {
            this.close();
        } else {
            this.open();
        }
    }
}

function abrirModal(modalId) {
    const modal = new Modal(modalId);
    modal.open();
}

function cerrarModal(modalId) {
    const modal = new Modal(modalId);
    modal.close();
}

document.addEventListener('DOMContentLoaded', () => {
    const modalTriggers = document.querySelectorAll('[data-modal-trigger]');
    
    modalTriggers.forEach(trigger => {
        trigger.addEventListener('click', () => {
            const modalId = trigger.getAttribute('data-modal-trigger');
            abrirModal(modalId);
        });
    });
});
