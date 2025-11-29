class MateriaManager {
    constructor() {
        this.idEliminar = null;
        this.init();
    }

    init() {
        this.setupListeners();
    }

    setupListeners() {
        const btnCrear = document.querySelector('[data-materia-crear]');
        if (btnCrear) {
            btnCrear.addEventListener('click', () => this.abrirCrear());
        }

        const botonesEditar = document.querySelectorAll('[data-materia-editar]');
        botonesEditar.forEach(btn => {
            btn.addEventListener('click', () => {
                const id = btn.getAttribute('data-materia-editar');
                this.abrirEditar(id);
            });
        });

        const botonesVer = document.querySelectorAll('[data-materia-ver]');
        botonesVer.forEach(btn => {
            btn.addEventListener('click', () => {
                const id = btn.getAttribute('data-materia-ver');
                this.abrirVer(id);
            });
        });

        const botonesEliminar = document.querySelectorAll('[data-materia-eliminar]');
        botonesEliminar.forEach(btn => {
            btn.addEventListener('click', () => {
                const id = btn.getAttribute('data-materia-eliminar');
                this.abrirEliminar(id);
            });
        });

        const formCrear = document.getElementById('crearMateriaForm');
        if (formCrear) {
            formCrear.addEventListener('submit', (e) => this.handleSubmitCrear(e));
        }

        const formEditar = document.getElementById('editarMateriaForm');
        if (formEditar) {
            formEditar.addEventListener('submit', (e) => this.handleSubmitEditar(e));
        }

        const formEliminar = document.getElementById('eliminarMateriaForm');
        if (formEliminar) {
            formEliminar.addEventListener('submit', (e) => this.handleSubmitEliminar(e));
        }
    }

    abrirCrear() { abrirModal('crearMateriaModal'); }

    abrirEditar(id) { this.cargarEdicion(id); abrirModal('editarMateriaModal'); }

    abrirVer(id) { this.cargarDetalle(id); abrirModal('verMateriaModal'); }

    abrirEliminar(id) { this.idEliminar = id; abrirModal('eliminarMateriaModal'); }

    handleSubmitCrear(e) {
        e.preventDefault();
        const form = e.target;
        const fd = new FormData(form);
        fetch(form.action, {
            method: 'POST',
            headers: { 'X-CSRFToken': this.getCSRFToken(form) },
            body: fd
        }).then(r => r.json()).then(data => {
            if (data.success) {
                cerrarModal('crearMateriaModal');
                this.notify('Materia creada', 'success');
                window.location.reload();
            } else {
                this.notify(data.error || 'Error al crear', 'danger');
            }
        }).catch(() => this.notify('Error de red', 'danger'));
    }

    handleSubmitEditar(e) {
        e.preventDefault();
        const form = e.target;
        const id = document.getElementById('materiaid')?.value;
        if (!id) return;
        const url = `/materia/${id}/editar/`;
        const fd = new FormData(form);
        fetch(url, {
            method: 'POST',
            headers: { 'X-CSRFToken': this.getCSRFToken(form) },
            body: fd
        }).then(r => r.json()).then(data => {
            if (data.success) {
                cerrarModal('editarMateriaModal');
                this.notify('Materia actualizada', 'success');
                setTimeout(() => window.location.reload(), 500);
            } else {
                this.notify(data.error || 'Error al actualizar', 'danger');
            }
        }).catch(err => {
            console.error('Error:', err);
            this.notify('Error de red', 'danger');
        });
    }

    handleSubmitEliminar(e) {
        e.preventDefault();
        if (!this.idEliminar) return;
        const form = e.target;
        const url = `/materia/${this.idEliminar}/eliminar/`;
        fetch(url, {
            method: 'POST',
            headers: { 'X-CSRFToken': this.getCSRFToken(form) }
        }).then(r => r.json()).then(data => {
            if (data.success) {
                cerrarModal('eliminarMateriaModal');
                this.notify('Materia eliminada', 'success');
                setTimeout(() => window.location.reload(), 500);
            } else {
                this.notify(data.error || 'Error al eliminar', 'danger');
            }
        }).catch(err => {
            console.error('Error:', err);
            this.notify('Error de red', 'danger');
        });
    }

    cargarDetalle(id) {
        const detalles = document.getElementById('detallesMateriaContent');
        if (detalles) detalles.textContent = 'Cargando...';
        fetch(`/materia/${id}/detalle/`).then(r => r.json()).then(data => {
            if (data.error) {
                detalles.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
            } else {
                detalles.innerHTML = `
                    <div class="mb-3">
                        <h5 class="fw-bold">${data.nombre}</h5>
                        <p class="text-muted">${data.descripcion || 'Sin descripción'}</p>
                        <div class="mt-3">
                            <strong>Estado:</strong><br>
                            <span class="badge ${data.estado_publicacion === 'publicada' ? 'bg-success' : 'bg-warning'} mt-2">
                                ${data.estado_publicacion === 'publicada' ? 'Publicada' : 'Borrador'}
                            </span>
                        </div>
                    </div>
                `;
            }
        }).catch(err => {
            console.error('Error:', err);
            if (detalles) detalles.innerHTML = '<div class="alert alert-danger">Error al cargar detalles</div>';
        });
    }

    cargarEdicion(id) {
        const inputId = document.getElementById('materiaid');
        if (inputId) inputId.value = id;
        fetch(`/materia/${id}/detalle/`).then(r => r.json()).then(data => {
            if (!data.error) {
                const nombreInput = document.getElementById('edit_nombre');
                if (nombreInput) nombreInput.value = data.nombre;
                const desc = document.getElementById('edit_descripcion');
                if (desc) desc.value = data.descripcion || '';
                const estado = document.getElementById('edit_estado');
                if (estado) estado.value = data.estado_publicacion;
            }
        }).catch(err => console.error('Error al cargar edición:', err));
    }

    getCSRFToken(form) {
        const input = form.querySelector('input[name="csrfmiddlewaretoken"]');
        if (input) return input.value;
        const name = 'csrftoken=';
        const cookies = document.cookie.split(';');
        for (let c of cookies) {
            c = c.trim();
            if (c.startsWith(name)) return c.substring(name.length);
        }
        return '';
    }

    notify(message, type) {
        if (window.showNotification) {
            window.showNotification(message, type);
        } else {
            alert(message);
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new MateriaManager();
});

function cargarMateria(id) {
    const manager = new MateriaManager();
    manager.cargarDetalle(id);
}

function cargarMateriaEdicion(id) {
    const manager = new MateriaManager();
    manager.cargarEdicion(id);
}

function confirmarEliminacion(id) {
    const manager = new MateriaManager();
    manager.abrirEliminar(id);
}
