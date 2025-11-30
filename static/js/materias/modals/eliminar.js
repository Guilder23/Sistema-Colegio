document.addEventListener('DOMContentLoaded', function() {
    const botonesEliminar = document.querySelectorAll('[data-eliminar-materia]');
    
    botonesEliminar.forEach(boton => {
        boton.addEventListener('click', function() {
            const materiaId = this.getAttribute('data-eliminar-materia');
            const materiaNombre = this.getAttribute('data-materia-nombre') || 'esta materia';
            
            if (confirm(`¿Estás seguro de que deseas eliminar "${materiaNombre}"? Esta acción no se puede deshacer.`)) {
                const formData = new FormData();
                formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));

                fetch(`/materia/${materiaId}/eliminar/`, {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Materia eliminada exitosamente');
                        location.reload();
                    } else {
                        alert('Error: ' + (data.error || 'Error desconocido'));
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Error de red: ' + error.message);
                });
            }
        });
    });
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
