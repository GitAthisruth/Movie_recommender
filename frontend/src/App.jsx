import { useState } from 'react'
import { Search } from 'lucide-react'

function App() {
  const [query, setQuery] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [results, setResults] = useState([])
  const [hasSearched, setHasSearched] = useState(false)
  const [error, setError] = useState(null)

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!query.trim()) return

    setIsLoading(true)
    setHasSearched(true)
    setError(null)
    
    try {
      const res = await fetch('/api/recommend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          text: query.trim(),
          limit: 5 // Defaulting to 5 because Tavily queries might be slow
        })
      })

      const data = await res.json()
      
      if (data.status === 'error') {
        throw new Error(data.error)
      }

      setResults(data.movies || [])
    } catch (err) {
      console.error(err)
      setError(err.message || 'Something went wrong while fetching recommendations.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <>
      <div className="hero-bg"></div>
      <div className="vignette"></div>

      <header className="app-header">
        <div className="logo">STREAMNET</div>
        <div className="header-right">
          <select className="lang-select" defaultValue="English">
            <option>English</option>
          </select>
          <button className="sign-in-btn">Sign In</button>
        </div>
      </header>

      <main className={`main-content ${hasSearched ? 'searched' : ''}`}>
        {!hasSearched && (
          <div className="hero-text">
            <h1>Unlimited movies, shows, and more</h1>
            <h2>Powered by AI. Discover exactly what you're in the mood for.</h2>
            <p>Ready to watch? Enter a genre, plot, or feeling to get recommendations.</p>
          </div>
        )}

        <form onSubmit={handleSearch} className="search-form">
          <div className="input-group">
            <input 
              type="text" 
              className="search-input" 
              placeholder="e.g., A funny sci-fi about time travel" 
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              required 
            />
            <button 
              type="submit" 
              className="search-btn"
              disabled={isLoading}
            >
              {isLoading ? 'Searching...' : 'Get Started'}
              {!isLoading && <Search size={20} />}
            </button>
          </div>
        </form>

        {isLoading && (
          <div className="loading-container">
            <div className="spinner"></div>
            <span>Finding the perfect movies...</span>
          </div>
        )}

        {!isLoading && error && (
          <div style={{color: 'var(--accent-red)', padding: '20px', background: 'rgba(255,0,0,0.1)', borderRadius: '8px'}}>
            An error occurred: {error}
          </div>
        )}

        {!isLoading && hasSearched && !error && (
          <div className="results-container">
            <h3 className="results-title">Top Recommendations</h3>
            
            {results.length === 0 ? (
              <div style={{color: 'var(--text-secondary)', padding: '20px'}}>
                No recommendations found for this query.
              </div>
            ) : (
              <div className="results-grid">
                {results.map((movie, index) => {
                  const tagsList = typeof movie.tags === 'string' 
                    ? movie.tags.split(',').map(t => t.trim()).slice(0, 4) 
                    : []

                  return (
                    <div key={index} className="movie-card" style={{ animationDelay: `${index * 0.05}s` }}>
                      {movie.image && (
                        <img 
                          src={movie.image} 
                          alt={`${movie.title} poster`} 
                          className="movie-poster"
                        />
                      )}
                      <div className="movie-rank">{index + 1}</div>
                      <h4 className="movie-title">{movie.title}</h4>
                      {movie.description && (
                        <p className="movie-description">{movie.description}</p>
                      )}
                      
                      {tagsList.length > 0 && (
                        <div className="movie-tags">
                          {tagsList.map((tag, i) => (
                            <span key={i} className="tag">{tag}</span>
                          ))}
                        </div>
                      )}
                    </div>
                  )
                })}
              </div>
            )}
          </div>
        )}
      </main>
    </>
  )
}

export default App
