document.addEventListener('DOMContentLoaded', function() {
    const botonesEditar = document.querySelectorAll('[data-editar-contenido]');
    
    botonesEditar.forEach(boton => {
        boton.addEventListener('click', function() {
            const contenidoId = this.getAttribute('data-editar-contenido');
            
            fetch(`/contenido/${contenidoId}/detalle/`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('contenido-id-editar').value = data.id;
                    document.getElementById('materia-editar').value = data.materia;
                    document.getElementById('titulo-editar').value = data.titulo;
                    document.getElementById('descripcion-editar').value = data.descripcion;
                    document.getElementById('tipo-editar').value = data.tipo;
                    document.getElementById('estado-editar').value = data.estado_publicacion;
                })
                .catch(error => console.error('Error al cargar detalles:', error));
        });
    });

    const formEditarContenido = document.getElementById('form-editar-contenido');
    if (!formEditarContenido) return;

    formEditarContenido.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const contenidoId = document.getElementById('contenido-id-editar').value;
        const titulo = document.getElementById('titulo-editar').value.trim();
        const descripcion = document.getElementById('descripcion-editar').value.trim();
        const tipo = document.getElementById('tipo-editar').value;
        const estado = document.getElementById('estado-editar').value;
        const archivo = document.getElementById('archivo-editar').files[0];

        if (!titulo) {
            alert('El título del contenido es requerido');
            return;
        }

        const formData = new FormData();
        formData.append('titulo', titulo);
        formData.append('descripcion', descripcion);
        formData.append('tipo', tipo);
        formData.append('estado_publicacion', estado);
        if (archivo) {
            formData.append('archivo', archivo);
        }
        formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));

        fetch(`/contenido/${contenidoId}/editar/`, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Contenido actualizado exitosamente');
                location.reload();
            } else {
                alert('Error: ' + (data.error || 'Error desconocido'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error de red: ' + error.message);
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
