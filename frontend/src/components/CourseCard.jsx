export default function CourseCard({ course, onBookmark }) {
  return (
    <div className="course-card">
      <div className="course-card-top">
        <div>
          <div className="course-title">{course.name}</div>
          <div className="course-sub">
            <span className="course-pill">{course.category}</span>
            <span className="course-pill course-pill-soft">{course.difficulty_level}</span>
          </div>
        </div>

        <div className="course-score">
          <div className="course-score-big">{course.matchPercentage}%</div>
          <div className="course-score-small">Match</div>
        </div>
      </div>

      <div className="course-body">
        <div className="course-desc">{course.description}</div>

        <div className="course-reasons">
          <div className="course-reasons-title">Why this course is recommended</div>
          <ul className="course-reasons-list">
            {(course.explanation?.why || []).slice(0, 3).map((w, idx) => (
              <li key={idx}>{w}</li>
            ))}
          </ul>
        </div>

        {course.career_opportunities ? (
          <div className="course-career">
            <b>Career opportunities:</b> {course.career_opportunities}
          </div>
        ) : null}
      </div>

      <div className="course-card-footer">
        <button
          className={course.bookmarked ? "ed-btn ed-btn-primary" : "ed-btn ed-btn-ghost"}
          onClick={() => onBookmark?.(course.courseId, !course.bookmarked)}
        >
          {course.bookmarked ? "Bookmarked" : "Bookmark"}
        </button>
        <div className="course-confidence">
          Confidence: <b>{course.confidence?.toFixed ? course.confidence.toFixed(2) : course.confidence}</b>
        </div>
      </div>
    </div>
  );
}

