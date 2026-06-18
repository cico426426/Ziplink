import { useState } from "react";
import "./App.css";

function App() {
  const [longUrl, setLongUrl] = useState("");
  const [shortUrl, setShortUrl] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setShortUrl("");

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/shorten?long_url=${encodeURIComponent(longUrl)}`,
        { method: "POST" }
      );
      const data = await response.json();
      setShortUrl(data.short_url);
    } catch {
      setError("發生錯誤，請確認後端是否啟動");
    }
  };

  return (
    <main className="app-shell">
      <section className="shortener-panel">
        <div className="panel-heading">
          <p className="eyebrow">URL Shortener</p>
          <h1>Ziplink</h1>
          <p className="subtitle">貼上長網址，產生一個方便分享的短連結。</p>
        </div>

        <form className="shortener-form" onSubmit={handleSubmit}>
          <label htmlFor="long-url">Long URL</label>
          <div className="input-row">
            <input
              id="long-url"
              type="url"
              placeholder="https://example.com/very/long/link"
              value={longUrl}
              onChange={(e) => setLongUrl(e.target.value)}
              required
            />
            <button type="submit">縮短</button>
          </div>
        </form>

        {shortUrl && (
          <div className="result-box">
            <span>短網址</span>
            <a href={`http://127.0.0.1:8000/${shortUrl}`} target="_blank" rel="noreferrer">
              {`http://127.0.0.1:8000/${shortUrl}`}
            </a>
          </div>
        )}

        {error && <p className="error-message">{error}</p>}
      </section>
    </main>
  );
}

export default App;
