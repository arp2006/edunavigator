import { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [stream, setStream] = useState(null);

  const SCALE = [
    { value: "Science", label: "Science" },
    { value: "Commerce", label: "Commerce" },
    { value: "Arts", label: "Arts/Humanities" }
  ];

  const onSubmit = async (e) => {
    if (stream==null) {
      setError("Please select a stream");
      setLoading(false);
      e.preventDefault();
      return;
    }
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await register({ name, email, password, stream });
      navigate("/quiz");
    } catch (err) {
      setError(err?.response?.data?.detail || "Register failed");
    } finally {
      setLoading(false);
    }
  };

  // useEffect(() => {
  //   console.log(name);
  //   console.log(email);
  //   console.log(password);
  //   console.log(stream);
    
  // }, [name, email, password, stream]);
  
  return (
    <div className="auth-page">
      <div className="auth-card">
        <h2>Create Account</h2>
        <p className="muted">Register to save quiz results and get AI-powered recommendations.</p>

        {error ? <div className="alert alert-danger">{error}</div> : null}

        <form onSubmit={onSubmit} className="auth-form">
          <label className="field">
            Name (optional)
            <input value={name} onChange={(e) => setName(e.target.value)} type="text" />
          </label>
          <label className="field">
            Email
            <input value={email} onChange={(e) => setEmail(e.target.value)} type="email" required />
          </label>
          <label className="field">
            Password
            <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" required />
          </label>
          <div className="stream-select">

            <div className="stream-title">
              Select Stream
            </div>
            <div className="scale-grid-register">
              {SCALE.map((s) => (
                <label key={s.value} className="scale-option-register">
                  <input
                    type="radio"
                    name="stream"
                    value={s.value}
                    checked={stream === s.value}
                    onChange={() => setStream(s.value)}
                  />
                  <span>{s.label}</span>
                </label>
              ))}
            </div>


          </div>

          <button className="ed-btn ed-btn-primary" disabled={loading}>
            {loading ? "Creating..." : "Register"}
          </button>
        </form>

        <div className="auth-links">
          <Link to="/login">Back to login</Link>
        </div>
      </div>
    </div>
  );
}

