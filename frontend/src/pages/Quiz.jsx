import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { api } from "../api";

const SCALE1to5 = [
  { value: null, label: "N/A" },
  { value: 1, label: "1" },
  { value: 2, label: "2" },
  { value: 3, label: "3" },
  { value: 4, label: "4" },
  { value: 5, label: "5" },
];

const SCALE_AGREE = [
  { value: 1, label: "Strongly Disagree" },
  { value: 2, label: "Disagree" },
  { value: 3, label: "Neutral" },
  { value: 4, label: "Agree" },
  { value: 5, label: "Strongly Agree" },
];

const SUBJECTS = {
  Science: ["math", "physics", "chemistry", "biology"],
  Commerce: ["accounts", "economics", "business"],
  Arts: ["history", "political_science", "psychology"],
};

const CATEGORY_QUESTIONS = {
  math: [
    "I enjoy solving logical puzzles.",
    "I am comfortable working with numbers.",
  ],
  science: [
    "I like understanding how things work.",
    "I enjoy experiments.",
  ],
  tech: [
    "I enjoy coding or building software.",
    "I like working on computers for long hours.",
  ],
  commerce: [
    "I am interested in business or finance.",
    "I enjoy planning strategies.",
  ],
  arts: [
    "I enjoy creative work like writing or design.",
    "I am interested in psychology or people.",
  ],
};

export default function Quiz() {
  const navigate = useNavigate();
  const { user } = useAuth();

  const stream = user?.stream || "Science";
  const profileId = user?.profile_id;

  const [responses, setResponses] = useState({});
  const [categoryResponses, setCategoryResponses] = useState({});
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const subjects = SUBJECTS[stream] || [];

  const setResponse = (subject, field, value) => {
    setResponses((prev) => ({
      ...prev,
      [subject]: { ...prev[subject], [field]: value },
    }));
  };

  const setCategoryResponse = (category, idx, value) => {
    setCategoryResponses((prev) => ({
      ...prev,
      [category]: { ...prev[category], [idx]: value },
    }));
  };

  // Subject is answered if user explicitly selected a value (including null = N/A)
  const subjectsComplete = subjects.every(
    (s) => s in responses && "interest" in (responses[s] || {}) && "performance" in (responses[s] || {})
  );

  // All category questions answered
  const categoryComplete = Object.entries(CATEGORY_QUESTIONS).every(
    ([cat, questions]) =>
      questions.every((_, idx) => categoryResponses[cat]?.[idx] != null)
  );

  const isComplete = subjectsComplete && categoryComplete;

  const onSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    if (!isComplete) {
      setError("Please answer all questions before submitting.");
      return;
    }

    setLoading(true);

    const payload = {
      profile_id: parseInt(profileId),
      // Only send subjects where the student actually rated (not N/A)
      responses: subjects
        .filter((subject) => responses[subject]?.interest !== null && responses[subject]?.performance !== null)
        .map((subject) => ({
          subject,
          interest: responses[subject].interest,
          performance: responses[subject].performance,
        })),
      extra: categoryResponses,
    };

    try {
      await api.post("/questionnaire/", payload);
      navigate("/dashboard");
    } catch (err) {
      const detail = err?.response?.data?.detail;
      let message = "Submission failed. Please try again.";
      if (Array.isArray(detail)) message = detail.map((e) => e.msg).join(", ");
      else if (typeof detail === "string") message = detail;
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <h2>Aptitude & Interest Quiz</h2>
      <p className="muted">
        Answer honestly. EduNavigator uses your responses to recommend the best bachelor's degrees for you.
      </p>

      {error && <div className="alert alert-danger">{error}</div>}

      <form onSubmit={onSubmit} className="quiz-form">

        {/* SUBJECT SECTION */}
        <div className="quiz-section">
          <div className="section-title">Core Subjects</div>
          <p className="section-desc">Rate your interest and performance in each subject (1 = low, 5 = high)</p>

          <div className="quiz-questions">
            {subjects.map((subject) => (
              <div key={subject} className="quiz-q">
                <div className="quiz-q-subject">
                  {subject.replace("_", " ").toUpperCase()}
                </div>

                <div className="quiz-q-title">
                  How much do you like {subject.replace("_", " ")}?
                </div>
                <div className="scale-grid">
                  {SCALE1to5.map((opt) => (
                    <label
                      key={opt.value}
                      className={`scale-option ${responses[subject]?.interest === opt.value ? "selected" : ""}`}
                    >
                      <input
                        type="radio"
                        name={`${subject}_interest`}
                        value={opt.value}
                        checked={responses[subject]?.interest === opt.value}
                        onChange={() => setResponse(subject, "interest", opt.value)}
                      />
                      <span>{opt.label}</span>
                    </label>
                  ))}
                </div>

                <div className="quiz-q-title">
                  How well do you perform in {subject.replace("_", " ")}?
                </div>
                <div className="scale-grid">
                  {SCALE1to5.map((opt) => (
                    <label
                      key={opt.value}
                      className={`scale-option ${responses[subject]?.performance === opt.value ? "selected" : ""}`}
                    >
                      <input
                        type="radio"
                        name={`${subject}_performance`}
                        value={opt.value}
                        checked={responses[subject]?.performance === opt.value}
                        onChange={() => setResponse(subject, "performance", opt.value)}
                      />
                      <span>{opt.label}</span>
                    </label>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* CATEGORY SECTION */}
        <div className="quiz-section">
          <div className="section-title">Your Preferences</div>
          <p className="section-desc">Tell us what you enjoy</p>

          {Object.entries(CATEGORY_QUESTIONS).map(([category, questions]) => (
            <div key={category} className="quiz-q">
              <div className="quiz-q-subject">{category.toUpperCase()}</div>

              {questions.map((q, idx) => (
                <div key={idx}>
                  <div className="quiz-q-title">{q}</div>
                  <div className="scale-grid-5">
                    {SCALE_AGREE.map((opt) => (
                      <label
                        key={opt.value}
                        className={`scale-option ${categoryResponses[category]?.[idx] === opt.value ? "selected" : ""}`}
                      >
                        <input
                          type="radio"
                          name={`${category}_${idx}`}
                          value={opt.value}
                          checked={categoryResponses[category]?.[idx] === opt.value}
                          onChange={() => setCategoryResponse(category, idx, opt.value)}
                        />
                        <span>{opt.label}</span>
                      </label>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          ))}
        </div>

        <div className="quiz-actions">
          <button
            className="ed-btn ed-btn-primary"
            disabled={loading || !isComplete}
          >
            {loading ? "Submitting..." : "Submit & Get Recommendations"}
          </button>

          {!isComplete && (
            <p className="muted" style={{ marginTop: "8px", fontSize: "13px" }}>
              Answer all questions to continue
            </p>
          )}
        </div>
      </form>
    </div>
  );
}