document.addEventListener('DOMContentLoaded', () => {
  const loginModal = document.getElementById('loginModal');
  const loginErrorAlert = document.getElementById('loginErrorAlert');
  const loginErrorMessage = document.getElementById('loginErrorMessage');
  const loginForm = document.getElementById('loginForm');

  if (loginModal) {
    // Limpiar el modal cuando se abre
    loginModal.addEventListener('show.bs.modal', () => {
      // Limpiar el formulario
      if (loginForm) loginForm.reset();
      
      // Limpiar y ocultar el mensaje de error
      if (loginErrorAlert) {
        loginErrorAlert.style.display = 'none';
        loginErrorAlert.classList.remove('show');
      }
      if (loginErrorMessage) {
        loginErrorMessage.textContent = '';
      }
    });

    // Limpiar cuando se cierra el modal
    loginModal.addEventListener('hide.bs.modal', () => {
      if (loginForm) loginForm.reset();
      if (loginErrorAlert) {
        loginErrorAlert.style.display = 'none';
        loginErrorAlert.classList.remove('show');
      }
    });
  }

  // Manejar mensajes de error de Django
  const messages = document.querySelectorAll('.messages .alert');
  if (messages.length > 0) {
    messages.forEach(msg => {
      // Si es un mensaje de error de login, mostrarlo en el modal
      if (msg.classList.contains('alert-danger') && msg.textContent.includes('Usuario o contraseña')) {
        if (loginModal && loginErrorAlert && loginErrorMessage) {
          // Mostrar el error en el modal
          loginErrorMessage.textContent = msg.textContent.trim();
          loginErrorAlert.style.display = 'block';
          loginErrorAlert.classList.add('show');

          // Abrir el modal
          const modal = new bootstrap.Modal(loginModal);
          modal.show();

          // Ocultar automáticamente después de 3 segundos
          setTimeout(() => {
            if (loginErrorAlert && loginErrorAlert.style.display !== 'none') {
              loginErrorAlert.classList.remove('show');
              setTimeout(() => {
                loginErrorAlert.style.display = 'none';
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
