document.addEventListener('DOMContentLoaded', function() {
    const botonesEliminar = document.querySelectorAll('[data-eliminar-contenido]');
    const modalEliminar = document.getElementById('modal-eliminar-contenido');
    const btnConfirmarEliminar = document.getElementById('btn-confirmar-eliminar-contenido');
    let contenidoIdActual = null;
    
    botonesEliminar.forEach(boton => {
        boton.addEventListener('click', function() {
            contenidoIdActual = this.getAttribute('data-eliminar-contenido');
            const contenidoTitulo = this.getAttribute('data-contenido-titulo') || 'este contenido';
            
            document.getElementById('eliminar-titulo-contenido').textContent = `"${contenidoTitulo}"`;
            const modal = new bootstrap.Modal(modalEliminar);
            modal.show();
        });
    });
    
    if (btnConfirmarEliminar) {
        btnConfirmarEliminar.addEventListener('click', function() {
            if (!contenidoIdActual) return;
            
            const formData = new FormData();
            formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));

            fetch(`/contenido/${contenidoIdActual}/eliminar/`, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const modal = bootstrap.Modal.getInstance(modalEliminar);
                    if (modal) modal.hide();
                    location.reload();
                } else {
                    console.error('Error:', data.error);
                }
            })
            .catch(error => {
                console.error('Error de red:', error);
            });
        });
    }
});

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
