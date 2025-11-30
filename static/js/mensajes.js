/**
 * Script para manejo de mensajes de alerta
 * Auto-cierre después de 5 segundos para mensajes de éxito
 * Los mensajes de error permanecen hasta que el usuario los cierre
 */

document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach((alert, index) => {
        // Agregar pequeño delay para cada alerta si hay múltiples
        setTimeout(() => {
            // Auto-cerrar solo mensajes de éxito después de 5 segundos
            if (alert.classList.contains('alert-success')) {
                setTimeout(() => {
                    const bsAlert = new bootstrap.Alert(alert);
                    bsAlert.close();
                }, 5000);
            }
            
            // Auto-cerrar mensajes de info después de 6 segundos
            if (alert.classList.contains('alert-info')) {
                setTimeout(() => {
                    const bsAlert = new bootstrap.Alert(alert);
                    bsAlert.close();
                }, 6000);
            }
            
            // Los mensajes de error y warning permanecen hasta que se cierren
        }, index * 200); // Delay de 200ms entre cada alerta
    });
});
