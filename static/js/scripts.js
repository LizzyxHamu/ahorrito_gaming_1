// Activar tooltips de Bootstrap
document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Inicializar contador de ofertas flash
    updateCountdown();
    setInterval(updateCountdown, 1000);

    // Configurar botón de volver arriba
    setupBackToTopButton();

    // Configurar manejo de cookies
    setupCookieConsent();
});

// Contador de ofertas flash
function updateCountdown() {
    var countdownElement = document.getElementById('countdown');
    if (countdownElement) {
        var time = countdownElement.textContent.split(':');
        var hours = parseInt(time[0]);
        var minutes = parseInt(time[1]);
        var seconds = parseInt(time[2]);

        seconds--;
        if (seconds < 0) {
            seconds = 59;
            minutes--;
            if (minutes < 0) {
                minutes = 59;
                hours--;
                if (hours < 0) {
                    hours = 12; // Reiniciar a 12 horas para demo
                    minutes = 0;
                    seconds = 0;
                }
            }
        }

        countdownElement.textContent = 
            (hours < 10 ? '0' + hours : hours) + ':' + 
            (minutes < 10 ? '0' + minutes : minutes) + ':' + 
            (seconds < 10 ? '0' + seconds : seconds);
    }
}

// Configuración del botón volver arriba
function setupBackToTopButton() {
    var backToTopButton = document.getElementById('backToTop');
    
    window.addEventListener('scroll', function() {
        if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
            backToTopButton.style.display = "flex";
        } else {
            backToTopButton.style.display = "none";
        }
    });

    backToTopButton.addEventListener('click', function(e) {
        e.preventDefault();
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Configuración del banner de cookies
function setupCookieConsent() {
    var cookieConsent = document.getElementById('cookieConsent');
    var acceptCookies = document.getElementById('acceptCookies');
    var rejectCookies = document.getElementById('rejectCookies');

    // Verificar si ya se aceptaron las cookies
    if (localStorage.getItem('cookiesAccepted')) {
        cookieConsent.style.display = 'none';
    }

    acceptCookies.addEventListener('click', function() {
        localStorage.setItem('cookiesAccepted', 'true');
        cookieConsent.style.display = 'none';
    });

    rejectCookies.addEventListener('click', function() {
        localStorage.setItem('cookiesRejected', 'true');
        cookieConsent.style.display = 'none';
    });
}

// Simulación de carrito de compras
document.addEventListener('DOMContentLoaded', function() {
    const addToCartButtons = document.querySelectorAll('.btn-primary:not([type="submit"])');
    
    addToCartButtons.forEach(button => {
        if (button.innerHTML.includes('Añadir')) {
            button.addEventListener('click', function() {
                const productName = this.closest('.card').querySelector('.card-title').textContent;
                showAddToCartNotification(productName);
            });
        }
    });
});

// Mostrar notificación de producto añadido al carrito
function showAddToCartNotification(productName) {
    // Crear elemento de notificación
    const notification = document.createElement('div');
    notification.className = 'position-fixed bottom-0 end-0 p-3 m-4 bg-success text-white rounded';
    notification.style.zIndex = '1060';
    notification.style.maxWidth = '300px';
    notification.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="fas fa-check-circle me-2"></i>
            <div>
                <strong>¡Producto añadido!</strong>
                <p class="mb-0">${productName} se ha añadido al carrito.</p>
            </div>
        </div>
    `;
    
    // Añadir al DOM
    document.body.appendChild(notification);
    
    // Eliminar después de 3 segundos
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transition = 'opacity 0.5s';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 500);
    }, 3000);
}


// ========================
// VALIDACIONES PARA EL MENU
// ========================

document.addEventListener('DOMContentLoaded', function() {
    // Toggle password visibility for login modal
    const toggleLoginPassword = document.getElementById('toggleLoginPassword');
    const loginPassword = document.getElementById('loginPassword');
    
    if (toggleLoginPassword && loginPassword) {
        toggleLoginPassword.addEventListener('click', function() {
            const type = loginPassword.getAttribute('type') === 'password' ? 'text' : 'password';
            loginPassword.setAttribute('type', type);
            this.querySelector('i').classList.toggle('fa-eye');
            this.querySelector('i').classList.toggle('fa-eye-slash');
        });
    }
    
    // Toggle password visibility for register modal
    const toggleRegisterPassword = document.getElementById('toggleRegisterPassword');
    const registerPassword = document.getElementById('registerPassword');
    
    if (toggleRegisterPassword && registerPassword) {
        toggleRegisterPassword.addEventListener('click', function() {
            const type = registerPassword.getAttribute('type') === 'password' ? 'text' : 'password';
            registerPassword.setAttribute('type', type);
            this.querySelector('i').classList.toggle('fa-eye');
            this.querySelector('i').classList.toggle('fa-eye-slash');
        });
    }
    
    // Password strength meter for register modal
    if (registerPassword) {
        const progressBar = document.querySelector('.progress-bar');
        
        registerPassword.addEventListener('input', function() {
            const value = registerPassword.value;
            let strength = 0;
            
            if (value.length >= 8) strength += 25;
            if (/[A-Z]/.test(value)) strength += 25;
            if (/[0-9]/.test(value)) strength += 25;
            if (/[^A-Za-z0-9]/.test(value)) strength += 25;
            
            progressBar.style.width = strength + '%';
            
            if (strength <= 25) {
                progressBar.className = 'progress-bar bg-danger';
            } else if (strength <= 50) {
                progressBar.className = 'progress-bar bg-warning';
            } else if (strength <= 75) {
                progressBar.className = 'progress-bar bg-info';
            } else {
                progressBar.className = 'progress-bar bg-success';
            }
        });
    }
});


// ===================================================================
// INCLUDES - esto es para poder unir los archivos htmls menú y footer
// ===================================================================
document.addEventListener('DOMContentLoaded', function() {
    // Función para cargar archivos HTML en elementos con atributo data-include
    function includeHTML() {
        const includes = document.querySelectorAll('[data-include]');
        
        includes.forEach(function(element) {
            const file = element.getAttribute('data-include');
            
            // Usar XMLHttpRequest que funciona mejor en entornos locales
            const xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function() {
                if (this.readyState == 4) {
                    if (this.status == 200) {
                        // Éxito - insertar el HTML
                        element.innerHTML = this.responseText;
                        
                        // Ejecutar scripts dentro del HTML incluido
                        const scripts = element.querySelectorAll('script');
                        scripts.forEach(script => {
                            const newScript = document.createElement('script');
                            
                            if (script.src) {
                                newScript.src = script.src;
                            } else {
                                newScript.textContent = script.textContent;
                            }
                            
                            document.head.appendChild(newScript);
                            script.remove();
                        });
                    } else {
                        // Error - mostrar mensaje
                        console.error(`Error al incluir ${file}: ${this.status}`);
                        element.innerHTML = `<p>Error al cargar el componente: ${file}</p>`;
                    }
                }
            };
            
            // Abrir la solicitud de forma síncrona para entornos locales
            xhr.open("GET", file, true);
            xhr.send();
        });
    }
    
    // Ejecutar la función para incluir HTML
    includeHTML();
});


