document.addEventListener('DOMContentLoaded', () => {
  const registroModal = document.getElementById('registroModal');
  if (registroModal) {
    registroModal.addEventListener('show.bs.modal', () => {
      const form = document.getElementById('registroForm');
      if (form) form.reset();
    });
  }
});
