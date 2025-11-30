// ============================================
// Script principal de la página de inicio
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('inicio.js cargado correctamente');

    // Inicializar funciones
    initScrollReveal();
    initFeatureCardHover();
});


// ============================================
// 1. Animación al hacer scroll (Reveal on Scroll)
// ============================================

function initScrollReveal() {
    const revealElementsList = document.querySelectorAll('.fade-up, .reveal');

    if (revealElementsList.length === 0) return; // Si no hay nada, evita errores

    const revealOnScroll = () => {
        revealElementsList.forEach(el => {
            const windowHeight = window.innerHeight;
            const elementTop = el.getBoundingClientRect().top;

            if (elementTop < windowHeight - 120) {
                el.classList.add("show", "active");
            }
        });
    };

    window.addEventListener("scroll", revealOnScroll);
    revealOnScroll(); // Ejecutar al cargar
}



// ============================================
// 2. Animación de hover para feature-cards
// ============================================

function initFeatureCardHover() {
    const cards = document.querySelectorAll('.feature-card');

    if (cards.length === 0) return; // Evita errores si no existen

    cards.forEach(card => {
        card.addEventListener('mousemove', () => {
            card.style.transform = "translateY(-8px) scale(1.03)";
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = "translateY(0) scale(1)";
        });
    });
}
