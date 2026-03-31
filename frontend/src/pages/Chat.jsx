import { useState, useEffect, useRef } from "react";
import { useAuth } from "../context/AuthContext";
import { api } from "../api";

const QUICK_QUERIES = [
  "I love coding and building things",
  "I'm interested in business and finance",
  "I enjoy science experiments and research",
  "I like writing and creative work",
];

export default function Chat() {
  const { user } = useAuth();

  // ✅ SINGLE SOURCE OF TRUTH
  const profileId = user?.profile_id || user?.profileId;

  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "Hi! I'm your EduNavigator advisor. Tell me about your interests.",
    },
  ]);

  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [error, setError] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const bottomRef = useRef(null);

  // 🔹 Load chat history
  useEffect(() => {
    if (!profileId) return;

    async function loadHistory() {
      try {
        console.log("Loading history for:", profileId);

        const res = await api.get(`/chat/history/${profileId}`);
        const history = res.data?.history || [];

        if (Array.isArray(history) && history.length > 0) {
          setMessages((prev) => [
            prev[0], // keep intro message
            ...history.map((h) => ({
              role: h.role,
              text: h.content || h.message || "",
            })),
          ]);
        }
      } catch (err) {
        console.error("History load failed:", err);
      }
    }

    loadHistory();
  }, [profileId]);

  // 🔹 Load initial recommendations
  useEffect(() => {
    if (!profileId) return;

    async function loadRecommendations() {
      try {
        console.log("Loading recs for:", profileId);

        const res = await api.get(`/recommend/${profileId}`);
        const data = res.data;

        let recs = [];

        if (Array.isArray(data)) recs = data;
        else if (Array.isArray(data?.recommendations))
          recs = data.recommendations;

        console.log("Initial recs:", recs);

        setRecommendations(recs);
      } catch (err) {
        console.error("Failed to load recommendations:", err);
      }
    }

    loadRecommendations();
  }, [profileId]);

  // 🔹 Auto scroll
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, sending]);

  // 🔹 Send message
  const sendMessage = async (text) => {
    const trimmed = String(text || input || "").trim();
    if (!trimmed || sending) return;

    if (!profileId) {
      setError("Profile missing. Complete onboarding.");
      return;
    }

    setError(null);
    setSending(true);
    setInput("");

    // add user message
    setMessages((prev) => [...prev, { role: "user", text: trimmed }]);

    try {
      console.log("Sending message:", trimmed);
      console.log("Using profileId:", profileId);

      const res = await api.post("/chat", {
        message: trimmed,
        profile_id: profileId, // ✅ FIXED
      });

      console.log("CHAT RESPONSE:", res.data);

      const reply = res?.data?.reply || "No response from server.";
      const raw = res?.data?.updated_recommendations;

      // ✅ STRICT VALIDATION
      let recs = [];

      if (Array.isArray(raw)) {
        recs = raw;
      } else if (Array.isArray(raw?.recommendations)) {
        recs = raw.recommendations;
      } else {
        console.error("Invalid recommendations format:", raw);
      }

      if (recs.length > 0) {
        setRecommendations(recs);
      }

      // add assistant reply
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: reply },
      ]);
    } catch (err) {
      console.error("Chat error:", err);

      const status = err?.response?.status;
      const detail = err?.response?.data?.detail;

      let msg = "Something went wrong.";
      if (status === 429) msg = "Too many requests.";
      else if (status === 401) msg = "Session expired.";
      else if (typeof detail === "string") msg = detail;

      setError(msg);

      // rollback message
      setMessages((prev) => prev.slice(0, -1));
      setInput(trimmed);
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="page">
      <h2>AI Chat Advisor</h2>

      {error && <div className="alert alert-danger">{error}</div>}

      <div className="chat-grid">
        {/* LEFT */}
        <div className="chat-panel">
          <div className="chat-messages">
            {messages.map((m, idx) => (
              <div key={idx} className={`chat-msg ${m.role}`}>
                {m.text}
              </div>
            ))}

            {sending && (
              <div className="chat-msg assistant">Typing...</div>
            )}

            <div ref={bottomRef} />
          </div>

          {/* quick queries */}
          <div className="chat-suggestions">
            {QUICK_QUERIES.map((q) => (
              <button
                key={q}
                className="chip-btn"
                onClick={() => sendMessage(q)}
                disabled={sending}
              >
                {q}
              </button>
            ))}
          </div>

          {/* input */}
          <div className="chat-input-row">
            <input
              className="field input"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Tell me about your interests..."
              disabled={sending}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  e.preventDefault();
                  sendMessage();
                }
              }}
            />

            <button
              onClick={() => sendMessage()}
              disabled={sending || !input.trim()}
            >
              {sending ? "Sending..." : "Send"}
            </button>
          </div>

          <div className="muted small">
            Profile ID: {profileId || "Missing"}
          </div>
        </div>

        {/* RIGHT */}
        <div className="chat-recs">
          <h3>Recommendations</h3>

          {recommendations.length === 0 ? (
            <p>No recommendations yet.</p>
          ) : (
            recommendations.map((r, i) => (
              <div key={i} className="course-card">
                <div>{r.degree_name}</div>
                <div>{r.field}</div>
                <div>Score: {Number(r.score).toFixed(2)}</div>
                {r.confidence && <div>{r.confidence}% match</div>}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}