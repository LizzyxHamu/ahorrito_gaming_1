// ===================================================================
// EVENTO PRINCIPAL: Se ejecuta cuando todo el HTML ha cargado
// ===================================================================
document.addEventListener('DOMContentLoaded', function() {
    
    // Inicializa todas las funcionalidades del sitio
    setupTooltips();
    setupCountdown();
    setupBackToTopButton();
    setupCookieConsent();
    setupSearchSuggestions(); // <--- LA NUEVA FUNCIÓN

});


// ===================================================================
// DEFINICIÓN DE FUNCIONES
// ===================================================================

/**
 * Activa los tooltips de Bootstrap en toda la página.
 */
function setupTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Actualiza el contador de ofertas flash cada segundo.
 */
function setupCountdown() {
    const countdownElement = document.getElementById('countdown');
    if (countdownElement) {
        // Función interna para actualizar el reloj
        const updateClock = function() {
            // ... (La lógica de tu contador se mantiene igual)
            var time = countdownElement.textContent.split(':');
            var hours = parseInt(time[0], 10) || 0;
            var minutes = parseInt(time[1], 10) || 0;
            var seconds = parseInt(time[2], 10) || 0;

            seconds--;
            if (seconds < 0) {
                seconds = 59;
                minutes--;
                if (minutes < 0) {
                    minutes = 59;
                    hours--;
                    if (hours < 0) {
                        hours = 12; // Reiniciar
                        minutes = 0;
                        seconds = 0;
                    }
                }
            }
            countdownElement.textContent = 
                (hours < 10 ? '0' + hours : hours) + ':' + 
                (minutes < 10 ? '0' + minutes : minutes) + ':' + 
                (seconds < 10 ? '0' + seconds : seconds);
        };
        // Llama a la función una vez y luego cada segundo
        updateClock();
        setInterval(updateClock, 1000);
    }
}

/**
 * Configura el botón para volver arriba en la página.
 */
function setupBackToTopButton() {
    const backToTopButton = document.getElementById('backToTop');
    if (backToTopButton) {
        window.addEventListener('scroll', function() {
            if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
                backToTopButton.style.display = "flex";
            } else {
                backToTopButton.style.display = "none";
            }
        });

        backToTopButton.addEventListener('click', function(e) {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
}

/**
 * Configura el banner de consentimiento de cookies.
 */
function setupCookieConsent() {
    const cookieConsent = document.getElementById('cookieConsent');
    const acceptCookies = document.getElementById('acceptCookies');
    
    if (cookieConsent && acceptCookies) {
        if (localStorage.getItem('cookiesAccepted')) {
            cookieConsent.style.display = 'none';
        }
        acceptCookies.addEventListener('click', function() {
            localStorage.setItem('cookiesAccepted', 'true');
            cookieConsent.style.display = 'none';
        });
    }
}

/**
 *  Configura las sugerencias en la barra de búsqueda.
 */
function setupSearchSuggestions() {
    const searchInput = document.getElementById('search-input');
    const suggestionsBox = document.getElementById('suggestions-box');

    if (searchInput && suggestionsBox) {
        searchInput.addEventListener('input', function() {
            const query = this.value;

            if (query.length < 2) {
                suggestionsBox.innerHTML = '';
                return;
            }

            // Llama a la nueva URL que creamos en Django
            fetch(`/search/suggestions/?term=${query}`)
                .then(response => response.json())
                .then(data => {
                    suggestionsBox.innerHTML = ''; // Limpia sugerencias anteriores
                    if (data.length > 0) {
                        data.forEach(item => {
                            const suggestionItem = document.createElement('a');
                            suggestionItem.href = `/search/?q=${encodeURIComponent(item)}`;
                            suggestionItem.className = 'list-group-item list-group-item-action bg-dark-ui text-light';
                            suggestionItem.textContent = item;
                            suggestionsBox.appendChild(suggestionItem);
                        });
                    }
                })
                .catch(error => console.error('Error fetching suggestions:', error));
        });

        // Oculta las sugerencias si el usuario hace clic en otra parte de la página
        document.addEventListener('click', function(event) {
            if (!searchInput.contains(event.target)) {
                suggestionsBox.innerHTML = '';
            }
        });
    }
}