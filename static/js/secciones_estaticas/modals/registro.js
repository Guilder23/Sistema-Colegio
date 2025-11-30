document.addEventListener('DOMContentLoaded', () => {
  const registroModal = document.getElementById('registroModal');
  const registroErrorAlert = document.getElementById('registroErrorAlert');
  const registroErrorMessage = document.getElementById('registroErrorMessage');
  const registroForm = document.getElementById('registroForm');

  if (registroModal) {
    // Limpiar el modal cuando se abre
    registroModal.addEventListener('show.bs.modal', () => {
      // Limpiar el formulario
      if (registroForm) registroForm.reset();
      
      // Limpiar y ocultar el mensaje de error
      if (registroErrorAlert) {
        registroErrorAlert.style.display = 'none';
        registroErrorAlert.classList.remove('show');
      }
      if (registroErrorMessage) {
        registroErrorMessage.textContent = '';
      }
    });

    // Limpiar cuando se cierra el modal
    registroModal.addEventListener('hide.bs.modal', () => {
      if (registroForm) registroForm.reset();
      if (registroErrorAlert) {
        registroErrorAlert.style.display = 'none';
        registroErrorAlert.classList.remove('show');
      }
    });
  }

  // Manejar mensajes de error de Django
  const messages = document.querySelectorAll('.messages .alert');
  if (messages.length > 0) {
    messages.forEach(msg => {
      // Si es un mensaje de error de registro
      if (msg.classList.contains('alert-danger')) {
        if (registroModal && registroErrorAlert && registroErrorMessage) {
          // Mostrar el error en el modal
          registroErrorMessage.textContent = msg.textContent.trim();
          registroErrorAlert.style.display = 'block';
          registroErrorAlert.classList.add('show');

          // Abrir el modal
          const modal = new bootstrap.Modal(registroModal);
          modal.show();

          // Ocultar automáticamente después de 3 segundos
          setTimeout(() => {
            if (registroErrorAlert && registroErrorAlert.style.display !== 'none') {
              registroErrorAlert.classList.remove('show');
              setTimeout(() => {
                registroErrorAlert.style.display = 'none';
              }, 150);
            }
          }, 3000);

          // Eliminar el mensaje de la página
          msg.style.display = 'none';
        }
      }
    });
  }
});
