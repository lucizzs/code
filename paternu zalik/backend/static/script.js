// Constants
const TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500';

// Load popular movies when page loads
document.addEventListener('DOMContentLoaded', () => {
    loadPopularMovies();
    loadFavoriteMovies();
});

// Load popular movies
async function loadPopularMovies() {
    try {
        const response = await fetch('/movies/popular/');
        const movies = await response.json();
        displayMovies(movies, 'popularMovies', true);
    } catch (error) {
        console.error('Error loading popular movies:', error);
    }
}

// Load favorite movies
async function loadFavoriteMovies() {
    try {
        const response = await fetch('/movies/favorites/');
        const movies = await response.json();
        displayMovies(movies, 'favoriteMovies', false);
    } catch (error) {
        if (error.status !== 404) {
            console.error('Error loading favorite movies:', error);
        }
    }
}

// Search movies
async function searchMovies() {
    const query = document.getElementById('searchInput').value;
    if (!query) return;

    try {
        const response = await fetch(`/movies/search/${encodeURIComponent(query)}`);
        const data = await response.json();
        displayMovies(data.results, 'popularMovies', true);
    } catch (error) {
        console.error('Error searching movies:', error);
    }
}

// Display movies in grid
function displayMovies(movies, containerId, isSearch) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';

    movies.forEach(movie => {
        const movieCard = document.createElement('div');
        movieCard.className = 'movie-card';
        
        const posterPath = movie.poster_path || movie.poster_url;
        const imageUrl = posterPath 
            ? `${TMDB_IMAGE_BASE_URL}${posterPath}`
            : '/static/no-poster.jpg';

        movieCard.innerHTML = `
            <img src="${imageUrl}" alt="${movie.title}">
            <div class="movie-info">
                <h3>${movie.title}</h3>
                <p>${movie.release_date || 'No date'}</p>
                <button 
                    class="favorite-btn"
                    onclick="${isSearch ? `addToFavorites(${JSON.stringify(movie).replace(/"/g, '&quot;')})` : `removeFromFavorites('${movie.movie_id}')`}"
                >
                    ${isSearch ? 'Add to Favorites' : 'Remove'}
                </button>
            </div>
        `;
        
        container.appendChild(movieCard);
    });
}

// Add movie to favorites
async function addToFavorites(movie) {
    try {
        const movieData = {
            movie_id: movie.id.toString(),
            title: movie.title,
            overview: movie.overview,
            release_date: movie.release_date,
            vote_average: movie.vote_average,
            poster_path: movie.poster_path
        };

        const response = await fetch('/movies/favorites/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(movieData)
        });

        if (response.ok) {
            await loadFavoriteMovies();
            alert('Movie added to favorites!');
        } else {
            const error = await response.json();
            alert(`Error: ${error.detail || 'Could not add to favorites'}`);
        }
    } catch (error) {
        console.error('Error adding to favorites:', error);
        alert('Error adding movie to favorites');
    }
}

// Remove movie from favorites
async function removeFromFavorites(movieId) {
    try {
        const response = await fetch(`/movies/favorites/${movieId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            await loadFavoriteMovies();
            alert('Movie removed from favorites!');
        } else {
            const error = await response.json();
            alert(`Error: ${error.detail || 'Could not remove from favorites'}`);
        }
    } catch (error) {
        console.error('Error removing from favorites:', error);
        alert('Error removing movie from favorites');
    }
} 