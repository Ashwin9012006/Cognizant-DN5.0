document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search-input');
    const resultsCount = document.getElementById('results-count');
    const cards = document.querySelectorAll('.course-card');
    const menuToggleBtn = document.getElementById('menu-toggle-btn');
    const mainNav = document.getElementById('main-nav');

    // Step 131: Mobile menu aria-expanded toggle
    if (menuToggleBtn && mainNav) {
        menuToggleBtn.addEventListener('click', () => {
            const isExpanded = menuToggleBtn.getAttribute('aria-expanded') === 'true';
            menuToggleBtn.setAttribute('aria-expanded', !isExpanded);
            mainNav.classList.toggle('open');
        });
    }

    // Step 129: Keyboard Accessibility (Enter key trigger on focused cards)
    cards.forEach(card => {
        const handleCardAction = () => {
            const isPressed = card.getAttribute('aria-pressed') === 'true';
            card.setAttribute('aria-pressed', !isPressed);
            const title = card.querySelector('h3').textContent;
            alert(`Selected Service: ${title}`);
        };

        // Click handler
        card.addEventListener('click', handleCardAction);

        // Keydown Enter handler for full keyboard navigability
        card.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                handleCardAction();
            }
        });
    });

    // Step 130: Dynamic Live Region update on search input
    if (searchInput && resultsCount) {
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase().trim();
            let visibleCount = 0;

            cards.forEach(card => {
                const text = card.textContent.toLowerCase();
                if (text.includes(query)) {
                    card.style.display = 'block';
                    visibleCount++;
                } else {
                    card.style.display = 'none';
                }
            });

            // Update live region text for screen readers
            resultsCount.textContent = `${visibleCount} service${visibleCount === 1 ? '' : 's'} found.`;
        });
    }
});
