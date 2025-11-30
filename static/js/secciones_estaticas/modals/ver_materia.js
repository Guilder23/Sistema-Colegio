// ==================== MODAL VER MATERIA ====================

let verMateriaModal;

document.addEventListener('DOMContentLoaded', function() {
    const modalElement = document.getElementById('verMateriaModal');
    if (modalElement) {
        verMateriaModal = new bootstrap.Modal(modalElement);
    }

    // Event listener para los botones "Ver"
    const botonesVer = document.querySelectorAll('button[data-materia-id]');
    
    botonesVer.forEach(boton => {
        boton.addEventListener('click', function(e) {
            e.preventDefault();
            const materiaId = this.dataset.materiaId;
            abrirVerMateriaModal(materiaId);
        });
    });
});

// Función para abrir el modal con los datos de la materia
function abrirVerMateriaModal(materiaId) {
    // Obtener la data del elemento clickeado
    const btnVer = document.querySelector(`button[data-materia-id="${materiaId}"]`);
    
    if (!btnVer) {
        console.error('Botón de ver no encontrado para materia:', materiaId);
        return;
    }

    const card = btnVer.closest('.card');
    if (!card) {
        console.error('Tarjeta no encontrada para materia:', materiaId);
        return;
    }

    const titulo = card.querySelector('.card-title').textContent.trim();
    const descripcion = card.dataset.descripcion || 'Sin descripción disponible';
    const profesor = card.querySelector('.fw-semibold').textContent.trim();
    
    try {
        var contenidos = JSON.parse(card.dataset.contenidos || '[]');
    } catch(e) {
        console.error('Error al parsear contenidos:', e);
        contenidos = [];
    }

    // Llenar el modal
    document.getElementById('modalMateriaTitle').textContent = titulo;
    document.getElementById('modalMateriaProfesor').textContent = `Por ${profesor}`;
    document.getElementById('modalMateriaDescripcion').textContent = descripcion;

    // Llenar contenidos
    const contenidosList = document.getElementById('modalContenidosList');
    
    if (contenidos.length === 0) {
        contenidosList.innerHTML = `
            <div class="alert alert-info text-center py-3 mb-0">
                <i class="fas fa-inbox fa-2x mb-2"></i>
                <p class="mb-0">No hay contenidos publicados para esta materia.</p>
            </div>
        `;
    } else {
        contenidosList.innerHTML = contenidos.map(contenido => `
            <div class="contenido-item">
                <h6>${contenido.titulo}</h6>
                <div class="d-flex align-items-center gap-2 mb-2">
                    <span class="badge">${contenido.tipo}</span>
                    <small class="text-muted">${contenido.fecha}</small>
                </div>
                <p>${contenido.descripcion}</p>
                ${contenido.tiene_archivo ? `
                    <a href="${contenido.archivo_url}" class="btn btn-outline-primary btn-sm mt-2" target="_blank">
                        <i class="fas fa-download"></i> Descargar
                    </a>
                ` : ''}
            </div>
        `).join('');
    }

    // Mostrar el modal
    if (verMateriaModal) {
        verMateriaModal.show();
    }
}
