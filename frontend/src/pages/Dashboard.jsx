import { useEffect, useMemo, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { api } from "../api";

export default function Dashboard() {
  const { user } = useAuth();

  const profileId = user?.profile_id || user?.profileId;

  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [category, setCategory] = useState("All");
  const [sortKey, setSortKey] = useState("score");

  useEffect(() => {
    async function load() {
      if (!profileId) return;

      setLoading(true);
      setError(null);

      try {
        const res = await api.get(`/recommend/${profileId}`);

        const data = (res.data.recommendations || []).map((r, idx) => ({
          id: idx,
          name: r.degree_name,
          field: r.field,
          discipline: r.discipline,
          type: r.type,
          score: r.score,

          // ✅ ADD THESE
          confidence: r.confidence,
          why: r.why,
        }));
        
        setRecommendations(data);
      } catch (err) {
        setError(
          err?.response?.data?.detail ||
          "Failed to load recommendations"
        );
      } finally {
        setLoading(false);
      }
    }

    load();
  }, [profileId]);

  // categories from fields
  const categories = useMemo(() => {
    const set = new Set(recommendations.map((r) => r.field).filter(Boolean));
    return ["All", ...Array.from(set)];
  }, [recommendations]);

  // filtering + sorting
  const filtered = useMemo(() => {
    let list = recommendations.slice();

    if (category !== "All") {
      list = list.filter((r) => r.field === category);
    }

    if (sortKey === "score") {
      list.sort((a, b) => b.score - a.score);
    }

    return list;
  }, [recommendations, category, sortKey]);

  return (
    <div className="page">
      <div className="page-head">
        <div>
          <h2>Recommendation Dashboard</h2>
          <p className="muted">
            Based on your aptitude and preferences.
          </p>
        </div>

        <div className="filters">
          <label className="field small-field">
            Field
            <select value={category} onChange={(e) => setCategory(e.target.value)}>
              {categories.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </label>

          <label className="field small-field">
            Sort
            <select value={sortKey} onChange={(e) => setSortKey(e.target.value)}>
              <option value="score">Score</option>
            </select>
          </label>
        </div>
      </div>

      {loading && <div className="muted">Loading recommendations...</div>}
      {error && <div className="alert alert-danger">{error}</div>}

      {!loading && !error && (
        <div className="cards-grid">
          {filtered.length === 0 ? (
            <p className="muted">No recommendations found.</p>
          ) : (
            filtered.map((item) => (
              <div key={item.id} className="card">
                <h3>{item.name}</h3>
                <p><strong>Field:</strong> {item.field}</p>
                <p><strong>Discipline:</strong> {item.discipline}</p>
                <p><strong>Type:</strong> {item.type}</p>
                <p>
                  <strong>Score:</strong> {item.score.toFixed(2)}
                </p>

                {/* ✅ CONFIDENCE */}
                {item.confidence !== undefined && (
                  <p>
                    <strong>Match:</strong> {item.confidence}%
                  </p>
                )}

                {/* ✅ WHY */}
                {item.why && (
                  <p className="muted small">
                    {item.why}
                  </p>
                )}
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}