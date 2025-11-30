document.addEventListener('DOMContentLoaded', () => {
  const loginModal = document.getElementById('loginModal');
  if (loginModal) {
    loginModal.addEventListener('show.bs.modal', () => {
      const form = document.getElementById('loginForm');
      if (form) form.reset();
    });
  }
});
