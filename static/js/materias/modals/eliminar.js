document.addEventListener('DOMContentLoaded', function() {
    const botonesEliminar = document.querySelectorAll('[data-eliminar-materia]');
    const modalEliminar = document.getElementById('modal-eliminar-materia');
    const btnConfirmarEliminar = document.getElementById('btn-confirmar-eliminar-materia');
    let materiaIdActual = null;
    
    botonesEliminar.forEach(boton => {
        boton.addEventListener('click', function() {
            materiaIdActual = this.getAttribute('data-eliminar-materia');
            const materiaNombre = this.getAttribute('data-materia-nombre') || 'esta materia';
            
            document.getElementById('eliminar-nombre-materia').textContent = `"${materiaNombre}"`;
            const modal = new bootstrap.Modal(modalEliminar);
            modal.show();
        });
    });
    
    if (btnConfirmarEliminar) {
        btnConfirmarEliminar.addEventListener('click', function() {
            if (!materiaIdActual) return;
            
            const formData = new FormData();
            formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));

            fetch(`/materia/${materiaIdActual}/eliminar/`, {
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
