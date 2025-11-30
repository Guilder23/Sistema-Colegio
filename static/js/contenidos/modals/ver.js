document.addEventListener('DOMContentLoaded', function() {
    const botonesVer = document.querySelectorAll('[data-ver-contenido]');
    
    botonesVer.forEach(boton => {
        boton.addEventListener('click', function() {
            const contenidoId = this.getAttribute('data-ver-contenido');
            
            fetch(`/contenido/${contenidoId}/detalle/`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('ver-titulo-contenido').textContent = data.titulo;
                    document.getElementById('ver-descripcion-contenido').textContent = data.descripcion || 'Sin descripción';
                    document.getElementById('ver-tipo-contenido').textContent = data.tipo;
                    document.getElementById('ver-estado-contenido').textContent = data.estado_publicacion === 'publico' ? 'Público' : 'Privado';
                    
                    // Mostrar modal
                    const modal = document.getElementById('modal-ver-contenido');
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
    console.log('Ver contenido modal.js cargado');
});
