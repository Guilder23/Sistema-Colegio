document.addEventListener('DOMContentLoaded', function() {
    const botonesEditar = document.querySelectorAll('[data-editar-materia]');
    
    botonesEditar.forEach(boton => {
        boton.addEventListener('click', function() {
            const materiaId = this.getAttribute('data-editar-materia');
            
            fetch(`/materia/${materiaId}/detalle/`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('materia-id-editar').value = data.id;
                    document.getElementById('nombre-editar').value = data.nombre;
                    document.getElementById('descripcion-editar').value = data.descripcion;
                    document.getElementById('estado-editar').value = data.estado_publicacion;
                })
                .catch(error => console.error('Error al cargar detalles:', error));
        });
    });

    const formEditarMateria = document.getElementById('form-editar-materia');
    if (!formEditarMateria) return;

    formEditarMateria.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const materiaId = document.getElementById('materia-id-editar').value;
        const nombre = document.getElementById('nombre-editar').value.trim();
        const descripcion = document.getElementById('descripcion-editar').value.trim();
        const estado = document.getElementById('estado-editar').value;

        if (!nombre) {
            alert('El nombre de la materia es requerido');
            return;
        }

        const formData = new FormData();
        formData.append('nombre', nombre);
        formData.append('descripcion', descripcion);
        formData.append('estado_publicacion', estado);
        formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));

        fetch(`/materia/${materiaId}/editar/`, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const modal = bootstrap.Modal.getInstance(document.getElementById('editarMateriaModal'));
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
