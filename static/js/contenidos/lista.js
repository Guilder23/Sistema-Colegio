class ContenidoManager {
    constructor() {
        this.idEliminar = null;
        this.init();
    }

    init() {
        this.setupListeners();
    }

    setupListeners() {
        // Botón crear contenido
        const btnCrear = document.querySelector('[data-contenido-crear]');
        if (btnCrear) {
            btnCrear.addEventListener('click', () => this.abrirCrear());
        }

        // Botones editar
        const botonesEditar = document.querySelectorAll('[data-contenido-editar]');
        botonesEditar.forEach(btn => {
            btn.addEventListener('click', () => {
                const id = btn.getAttribute('data-contenido-editar');
                this.abrirEditar(id);
            });
        });

        // Botones ver
        const botonesVer = document.querySelectorAll('[data-contenido-ver]');
        botonesVer.forEach(btn => {
            btn.addEventListener('click', () => {
                const id = btn.getAttribute('data-contenido-ver');
                this.abrirVer(id);
            });
        });

        // Botones eliminar
        const botonesEliminar = document.querySelectorAll('[data-contenido-eliminar]');
        botonesEliminar.forEach(btn => {
            btn.addEventListener('click', () => {
                const id = btn.getAttribute('data-contenido-eliminar');
                this.abrirEliminar(id);
            });
        });

        // Formulario crear
        const formCrear = document.getElementById('crearContenidoForm');
        if (formCrear) {
            formCrear.addEventListener('submit', (e) => this.handleSubmitCrear(e));
        }

        // Formulario editar
        const formEditar = document.getElementById('editarContenidoForm');
        if (formEditar) {
            formEditar.addEventListener('submit', (e) => this.handleSubmitEditar(e));
        }

        // Botón confirmar eliminar
        const formEliminar = document.getElementById('eliminarContenidoForm');
        if (formEliminar) {
            formEliminar.addEventListener('submit', (e) => this.handleSubmitEliminar(e));
        }

        // Filtro de materias
        const filterMateria = document.getElementById('filter-materia');
        if (filterMateria) {
            filterMateria.addEventListener('change', () => this.filtrarPorMateria());
        }

        // Filtro de tipo
        const filterTipo = document.getElementById('filter-tipo');
        if (filterTipo) {
            filterTipo.addEventListener('change', () => this.filtrarPorTipo());
        }
    }

    abrirCrear() { abrirModal('crearContenidoModal'); }

    abrirEditar(id) { this.cargarEdicion(id); abrirModal('editarContenidoModal'); }

    abrirVer(id) { this.cargarDetalle(id); abrirModal('verContenidoModal'); }

    abrirEliminar(id) { this.idEliminar = id; abrirModal('eliminarContenidoModal'); }

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
                cerrarModal('crearContenidoModal');
                this.notify('Contenido creado', 'success');
                window.location.reload();
            } else {
                this.notify(data.error || 'Error al crear', 'danger');
            }
        }).catch(() => this.notify('Error de red', 'danger'));
    }

    handleSubmitEditar(e) {
        e.preventDefault();
        const form = e.target;
        const id = document.getElementById('contenidoid')?.value;
        if (!id) return;
        const url = `/contenido/${id}/editar/`;
        const fd = new FormData(form);
        fetch(url, {
            method: 'POST',
            headers: { 'X-CSRFToken': this.getCSRFToken(form) },
            body: fd
        }).then(r => r.json()).then(data => {
            if (data.success) {
                cerrarModal('editarContenidoModal');
                this.notify('Contenido actualizado', 'success');
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
        const url = `/contenido/${this.idEliminar}/eliminar/`;
        fetch(url, {
            method: 'POST',
            headers: { 'X-CSRFToken': this.getCSRFToken(form) }
        }).then(r => r.json()).then(data => {
            if (data.success) {
                cerrarModal('eliminarContenidoModal');
                this.notify('Contenido eliminado', 'success');
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
        const detalles = document.getElementById('detallesContenidoContent');
        if (detalles) detalles.textContent = 'Cargando...';
        fetch(`/contenido/${id}/detalle/`).then(r => r.json()).then(data => {
            if (data.error) {
                detalles.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
            } else {
                detalles.innerHTML = `
                    <div class="mb-3">
                        <h5 class="fw-bold">${data.titulo}</h5>
                        <p class="text-muted">${data.descripcion || 'Sin descripción'}</p>
                        <div class="mt-3">
                            <p><strong>Tipo:</strong> <span class="badge bg-info">${data.tipo}</span></p>
                            <p><strong>Estado:</strong> <span class="badge ${data.estado_publicacion === 'publico' ? 'bg-success' : 'bg-warning'}">${data.estado_publicacion}</span></p>
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
        const inputId = document.getElementById('contenidoid');
        if (inputId) inputId.value = id;
        fetch(`/contenido/${id}/detalle/`).then(r => r.json()).then(data => {
            if (!data.error) {
                const materia = document.getElementById('edit_materia');
                if (materia) materia.value = data.materia;
                const titulo = document.getElementById('edit_titulo');
                if (titulo) titulo.value = data.titulo;
                const desc = document.getElementById('edit_descripcion');
                if (desc) desc.value = data.descripcion || '';
                const tipo = document.getElementById('edit_tipo');
                if (tipo) tipo.value = data.tipo;
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

// Inicializar al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    new ContenidoManager();
});

function cargarContenido(id) {
    const manager = new ContenidoManager();
    manager.cargarDetalle(id);
}

function cargarContenidoEdicion(id) {
    const manager = new ContenidoManager();
    manager.cargarEdicion(id);
}

function confirmarEliminacionContenido(id) {
    const manager = new ContenidoManager();
    manager.abrirEliminar(id);
}
