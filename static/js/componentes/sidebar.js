document.addEventListener('DOMContentLoaded', () => {
  const sidebar = document.getElementById('sidebarMenu');
  const openBtn = document.getElementById('openSidebar');
  const closeBtn = document.getElementById('closeSidebar');

  const open = () => { if (sidebar) sidebar.classList.add('show'); };
  const close = () => { if (sidebar) sidebar.classList.remove('show'); };

  if (openBtn) openBtn.addEventListener('click', open);
  if (closeBtn) closeBtn.addEventListener('click', close);

  if (sidebar) {
    const links = sidebar.querySelectorAll('.nav-link');
    links.forEach(link => link.addEventListener('click', () => {
      if (window.innerWidth <= 768) close();
    }));
  }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') close();
  });
});
