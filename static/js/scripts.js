document.addEventListener('DOMContentLoaded', function() {

    // Se mantienen las funcionalidades que sí son útiles y correctas.
    setupTooltips();
    setupSearchSuggestions();
});


/**
 * Inicializa los tooltips de Bootstrap en la página.
 */
function setupTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Configura la funcionalidad de sugerencias de búsqueda en el input de búsqueda.
 */
function setupSearchSuggestions() {
    const searchInput = document.getElementById('search-input');
    const suggestionsBox = document.getElementById('suggestions-box');

    if (searchInput && suggestionsBox) {
        searchInput.addEventListener('input', function() {
            const query = this.value;
            if (query.length < 2) {
                suggestionsBox.innerHTML = '';
                suggestionsBox.classList.remove('d-block');
                return;
            }

            fetch(`/search/suggestions/?term=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    suggestionsBox.innerHTML = '';
                    if (data.length > 0) {
                        suggestionsBox.classList.add('d-block');
                        data.forEach(item => {
                            const suggestionItem = document.createElement('a');
                            suggestionItem.href = `/search/?q=${encodeURIComponent(item)}`;
                            suggestionItem.className = 'list-group-item list-group-item-action bg-dark-ui text-light';
                            suggestionItem.textContent = item;
                            suggestionsBox.appendChild(suggestionItem);
                        });
                    } else {
                        suggestionsBox.classList.remove('d-block');
                    }
                })
                .catch(error => {
                    console.error('Error fetching search suggestions:', error);
                    suggestionsBox.classList.remove('d-block');
                });
        });

        // Ocultar sugerencias cuando se hace clic fuera del área de búsqueda
        document.addEventListener('click', function(event) {
            if (!searchInput.contains(event.target) && !suggestionsBox.contains(event.target)) {
                suggestionsBox.innerHTML = '';
                suggestionsBox.classList.remove('d-block');
            }
        });
    }
}