document.addEventListener('DOMContentLoaded', function() {
    const botonesVer = document.querySelectorAll('[data-ver-materia]');
    
    botonesVer.forEach(boton => {
        boton.addEventListener('click', function() {
            const materiaId = this.getAttribute('data-ver-materia');
            
            fetch(`/materia/${materiaId}/detalle/`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('ver-nombre-materia').textContent = data.nombre;
                    document.getElementById('ver-descripcion-materia').textContent = data.descripcion || 'Sin descripción';
                    document.getElementById('ver-estado-materia').textContent = data.estado_publicacion === 'publicada' ? 'Publicada' : 'Borrador';
                    
                    // Mostrar modal
                    const modal = document.getElementById('modal-ver-materia');
                    if (modal) {
                        const bsModal = new bootstrap.Modal(modal);
                        bsModal.show();
                    }
                })
                .catch(error => {
                    console.error('Error al cargar detalles:', error);
                    alert('Error al cargar los detalles');
                });
        });
    });
});
document.addEventListener('DOMContentLoaded', function() {
    console.log('Ver materia modal.js cargado');
});
