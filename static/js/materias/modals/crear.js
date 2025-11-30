document.addEventListener('DOMContentLoaded', function() {
    const formCrearMateria = document.getElementById('form-crear-materia');
    if (!formCrearMateria) return;

    formCrearMateria.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const nombre = document.getElementById('nombre-crear').value.trim();
        const descripcion = document.getElementById('descripcion-crear').value.trim();
        const estado = document.getElementById('estado-crear').value;

        if (!nombre) {
            alert('El nombre de la materia es requerido');
            return;
        }

        const formData = new FormData();
        formData.append('nombre', nombre);
        formData.append('descripcion', descripcion);
        formData.append('estado_publicacion', estado);
        formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));

        fetch('/materia/crear/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                formCrearMateria.reset();
                const modal = bootstrap.Modal.getInstance(document.getElementById('crearMateriaModal'));
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
