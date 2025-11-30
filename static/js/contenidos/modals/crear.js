document.addEventListener('DOMContentLoaded', function() {
    const formCrearContenido = document.getElementById('form-crear-contenido');
    if (!formCrearContenido) return;

    formCrearContenido.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const materia = document.getElementById('materia-crear').value;
        const titulo = document.getElementById('titulo-crear').value.trim();
        const descripcion = document.getElementById('descripcion-crear').value.trim();
        const tipo = document.getElementById('tipo-crear').value;
        const estado = document.getElementById('estado-crear').value;
        const archivo = document.getElementById('archivo-crear').files[0];

        if (!materia) {
            alert('Debes seleccionar una materia');
            return;
        }

        if (!titulo) {
            alert('El título del contenido es requerido');
            return;
        }

        const formData = new FormData();
        formData.append('materia', materia);
        formData.append('titulo', titulo);
        formData.append('descripcion', descripcion);
        formData.append('tipo', tipo);
        formData.append('estado_publicacion', estado);
        if (archivo) {
            formData.append('archivo', archivo);
        }
        formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));

        fetch('/contenido/crear/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Contenido creado exitosamente');
                formCrearContenido.reset();
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
