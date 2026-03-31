import { useEffect, useState } from "react";
import { api } from "../api";

export default function Admin() {
  const [stats, setStats] = useState(null);
  const [users, setUsers] = useState([]);
  const [quizResults, setQuizResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [form, setForm] = useState({
    name: "",
    category: "",
    difficulty_level: "Beginner",
    career_opportunities: "",
    description: "",
    popularity_score: 70,
    skills_required: "Python, SQL",
  });
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    async function load() {
      setLoading(true);
      setError(null);
      try {
        const [statsRes, usersRes, quizzesRes] = await Promise.all([
          api.get("/admin/stats"),
          api.get("/admin/users"),
          api.get("/admin/quiz-results"),
        ]);
        setStats(statsRes.data.stats);
        setUsers(usersRes.data.users || []);
        setQuizResults(quizzesRes.data.quizResults || []);
      } catch (err) {
        setError(err?.response?.data?.error || "Failed to load stats");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const submitCourse = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError(null);
    try {
      await api.post("/admin/course", {
        name: form.name,
        category: form.category,
        difficulty_level: form.difficulty_level,
        career_opportunities: form.career_opportunities,
        description: form.description,
        popularity_score: Number(form.popularity_score),
        skills_required: form.skills_required
          .split(",")
          .map((s) => s.trim())
          .filter(Boolean),
      });
      setForm((prev) => ({ ...prev, name: "", category: "", description: "" }));
      const res = await api.get("/admin/stats");
      setStats(res.data.stats);
      // eslint-disable-next-line no-alert
      alert("Course added successfully!");
    } catch (err) {
      setError(err?.response?.data?.error || "Failed to add course");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="page">
      <h2>Admin Panel</h2>
      <p className="muted">Add courses and analyze recommendation trends (basic analytics).</p>

      {error ? <div className="alert alert-danger">{error}</div> : null}

      {loading ? (
        <div className="muted">Loading admin stats...</div>
      ) : stats ? (
        <div className="admin-grid">
          <div className="admin-card">
            <div className="admin-metric">
              <div className="admin-metric-title">Users</div>
              <div className="admin-metric-value">{stats.userCount}</div>
            </div>
            <div className="admin-metric">
              <div className="admin-metric-title">Courses</div>
              <div className="admin-metric-value">{stats.courseCount}</div>
            </div>
            <div className="admin-metric">
              <div className="admin-metric-title">Quiz Results</div>
              <div className="admin-metric-value">{stats.quizCount}</div>
            </div>
            <div className="admin-metric">
              <div className="admin-metric-title">Avg Recommendation Score</div>
              <div className="admin-metric-value">{stats.avgRecommendationScore}</div>
            </div>
          </div>

          <div className="admin-card">
            <div className="section-title">Top Categories in Recommendations</div>
            <div className="bar-list">
              {stats.topCategories?.map((c) => (
                <div key={c.category} className="bar-row">
                  <div className="bar-label">{c.category}</div>
                  <div className="bar-track">
                    <div className="bar-fill" style={{ width: `${Math.min(100, (c.recCount / Math.max(1, stats.topCategories[0]?.recCount || 1)) * 100)}%` }} />
                  </div>
                  <div className="bar-value">{c.recCount}</div>
                </div>
              ))}
              {!stats.topCategories?.length ? <div className="muted">No recommendation data yet.</div> : null}
            </div>
          </div>
        </div>
      ) : null}

      {!loading ? (
        <div className="admin-grid" style={{ marginTop: 14 }}>
          <div className="admin-card">
            <div className="section-title" style={{ marginTop: 0 }}>Recent Users</div>
            <div className="bar-list">
              {users.map((u) => (
                <div key={u.id} className="bar-row" style={{ gridTemplateColumns: "1fr 1fr 0" }}>
                  <div className="bar-label">
                    <b>#{u.id}</b> {u.email}
                  </div>
                  <div className="muted" style={{ fontSize: 12 }}>
                    {u.stream} • {u.career_goals ? String(u.career_goals).slice(0, 30) : "—"}
                  </div>
                  <div />
                </div>
              ))}
              {!users.length ? <div className="muted">No users yet.</div> : null}
            </div>
          </div>

          <div className="admin-card">
            <div className="section-title" style={{ marginTop: 0 }}>Recent Quiz Responses</div>
            <div className="bar-list">
              {quizResults.map((q) => (
                <div key={q.id} className="bar-row" style={{ gridTemplateColumns: "1fr 1fr 0" }}>
                  <div className="bar-label">
                    <b>Quiz #{q.id}</b> (User #{q.user_id})
                  </div>
                  <div className="muted" style={{ fontSize: 12 }}>
                    Score: {q.total_score}
                  </div>
                  <div />
                </div>
              ))}
              {!quizResults.length ? <div className="muted">No quiz responses yet.</div> : null}
            </div>
          </div>
        </div>
      ) : null}

      <div className="section-title">Add New Course</div>
      <form onSubmit={submitCourse} className="course-form">
        <div className="form-grid">
          <label className="field form-span-2">
            Course Name
            <input value={form.name} onChange={(e) => setForm((p) => ({ ...p, name: e.target.value }))} required />
          </label>

          <label className="field">
            Category
            <input value={form.category} onChange={(e) => setForm((p) => ({ ...p, category: e.target.value }))} required />
          </label>

          <label className="field">
            Difficulty Level
            <select value={form.difficulty_level} onChange={(e) => setForm((p) => ({ ...p, difficulty_level: e.target.value }))}>
              <option>Beginner</option>
              <option>Intermediate</option>
              <option>Advanced</option>
            </select>
          </label>

          <label className="field">
            Popularity Score (0..100)
            <input
              type="number"
              min="0"
              max="100"
              value={form.popularity_score}
              onChange={(e) => setForm((p) => ({ ...p, popularity_score: e.target.value }))}
              required
            />
          </label>

          <label className="field form-span-2">
            Career Opportunities
            <input
              value={form.career_opportunities}
              onChange={(e) => setForm((p) => ({ ...p, career_opportunities: e.target.value }))}
              placeholder="Example: AI Engineer, ML Intern"
            />
          </label>

          <label className="field form-span-2">
            Skills Required (comma separated)
            <input
              value={form.skills_required}
              onChange={(e) => setForm((p) => ({ ...p, skills_required: e.target.value }))}
              placeholder="Example: Python, SQL, TensorFlow"
            />
          </label>

          <label className="field form-span-2">
            Description
            <textarea
              value={form.description}
              onChange={(e) => setForm((p) => ({ ...p, description: e.target.value }))}
              rows={4}
              placeholder="Course description..."
            />
          </label>
        </div>

        <button className="ed-btn ed-btn-primary" disabled={saving}>
          {saving ? "Adding..." : "Add Course"}
        </button>
      </form>
    </div>
  );
}

