document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search-input');
    const loading = document.getElementById('loading');
    const resultsContainer = document.getElementById('results-container');
    const resultsGrid = document.getElementById('results-grid');
    const mainContent = document.querySelector('.main-content');
    const heroText = document.getElementById('hero-text');

    searchForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const query = searchInput.value.trim();
        if (!query) return;

        // UI transitions
        mainContent.classList.add('searched');
        heroText.style.opacity = '0';
        heroText.style.height = '0';
        heroText.style.overflow = 'hidden';
        heroText.style.marginBottom = '0';
        
        resultsContainer.classList.add('hidden');
        loading.classList.remove('hidden');
        resultsGrid.innerHTML = '';

        try {
            const response = await fetch('/api/recommend', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text: query,
                    limit: 15
                })
            });

            const data = await response.json();

            if (data.status === 'error') {
                throw new Error(data.error);
            }

            renderResults(data.movies);
        } catch (error) {
            console.error('Error fetching recommendations:', error);
            resultsGrid.innerHTML = `<div style="color: var(--accent-red); padding: 20px;">An error occurred. Please try again. (${error.message})</div>`;
            resultsContainer.classList.remove('hidden');
        } finally {
            loading.classList.add('hidden');
        }
    });

    function renderResults(movies) {
        if (!movies || movies.length === 0) {
            resultsGrid.innerHTML = '<div style="color: var(--text-secondary); padding: 20px;">No recommendations found for this query.</div>';
            resultsContainer.classList.remove('hidden');
            return;
        }

        movies.forEach((movie, index) => {
            const card = document.createElement('div');
            card.className = 'movie-card';
            card.style.animationDelay = `${index * 0.05}s`;
            
            // Format tags nicely
            let tagsHtml = '';
            if (movie.tags) {
                // Assuming tags might be a space-separated or comma-separated string,
                // let's try to split them nicely if they are simple words, 
                // or just display them. Adjust based on your db format.
                const tagsList = typeof movie.tags === 'string' 
                    ? movie.tags.split(',').map(t => t.trim()).slice(0, 4) 
                    : [];
                
                tagsHtml = `<div class="movie-tags">
                    ${tagsList.map(tag => `<span class="tag">${tag}</span>`).join('')}
                </div>`;
            }

            card.innerHTML = `
                ${movie.image ? '<img src="' + movie.image + '" alt="' + movie.title + ' poster" style="width: 100%; height: 350px; object-fit: cover; border-radius: 4px; margin-bottom: 12px;" />' : ''}
                <div class="movie-rank">${index + 1}</div>
                <h4 class="movie-title">${movie.title}</h4>
                ${movie.description ? '<p style="font-size: 0.85rem; color: #ccc; margin-bottom: 12px; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden;">' + movie.description + '</p>' : ''}
                ${tagsHtml}
            `;
            resultsGrid.appendChild(card);
        });

        resultsContainer.classList.remove('hidden');
    }
});
