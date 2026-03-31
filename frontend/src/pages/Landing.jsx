import { useNavigate } from "react-router-dom";
import "./Landing.css";

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div className="landing">

      {/* BACKGROUND GLOW */}
      <div className="bg-glow"></div>

      {/* NAVBAR */}
      <nav className="navbar">
        <h2 className="logo">EduNavigator</h2>
        <div className="nav-buttons">
          <button className="login" onClick={() => navigate("/login")}>
            Login
          </button>
          <button className="signup" onClick={() => navigate("/register")}>
            Get Started
          </button>
        </div>
      </nav>

      {/* HERO */}
      <section className="hero">
        <div className="hero-content">

          <span className="badge">AI Powered Platform</span>

          <h1>AI-Powered Course Recommendations</h1>

          <p>
            Discover the best courses tailored to your skills, interests, and
            career goals using intelligent and explainable recommendations.
          </p>

          <div className="hero-buttons">
            <button className="primary" onClick={() => navigate("/register")}>
              Get Recommendations
            </button>
            <button className="secondary" onClick={() => navigate("/dashboard")}>
              View Dashboard
            </button>
          </div>

        </div>
      </section>

      {/* FEATURES */}
      <section className="features">
        <div className="card">
          <h3>Explainable AI</h3>
          <p>Understand why each course is recommended based on your profile.</p>
        </div>

        <div className="card">
          <h3>Skill-Based Matching</h3>
          <p>Recommendations tailored to your strengths and learning goals.</p>
        </div>

        <div className="card">
          <h3>Career Insights</h3>
          <p>Explore real career paths linked with each course.</p>
        </div>
      </section>

      {/* STATS */}
      <section className="stats">
        <div className="stat">
          <h2>1000+</h2>
          <p>Courses Available</p>
        </div>
        <div className="stat">
          <h2>500+</h2>
          <p>Students Guided</p>
        </div>
        <div className="stat">
          <h2>95%</h2>
          <p>Accuracy Rate</p>
        </div>
      </section>

      {/* HOW IT WORKS */}
      <section className="steps">
        <h2>How It Works</h2>

        <div className="step-container">
          <div className="step">
            <span>1</span>
            <p>Take a quick aptitude quiz</p>
          </div>

          <div className="step">
            <span>2</span>
            <p>AI analyzes your interests & skills</p>
          </div>

          <div className="step">
            <span>3</span>
            <p>Get personalized course recommendations</p>
          </div>
        </div>
      </section>

      {/* FINAL CTA */}
      <section className="final-cta">
        <h2>Start Your Career Journey Today</h2>
        <button onClick={() => navigate("/register")}>
          Get Started Now
        </button>
      </section>

      {/* FOOTER */}
      <footer className="footer">
        <p>© 2026 EduNavigator | AI Course Recommendation System</p>
      </footer>

    </div>
  );
}