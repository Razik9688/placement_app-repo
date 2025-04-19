#placement_app.py
import streamlit as st
import pandas as pd
import pymysql

# ----------------------------- MYSQL CONFIG -----------------------------
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Mysql@4321',
    'database': 'placement_db'
}

# ----------------------------- DATABASE CONNECTION -----------------------------
class DatabaseConnection:
    def __init__(self):
        self.conn = pymysql.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)

    def fetchone(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def fetchall(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

# ----------------------------- MENU 1: OVERVIEW -----------------------------
def show_overview():
    st.header("📊 Overview of Placement Data")
    db = DatabaseConnection()

    # Get totals
    total_students = db.fetchone("SELECT COUNT(*) as total_students FROM students")['total_students']
    total_placed = db.fetchone("SELECT COUNT(*) as total_placed FROM placements WHERE placement_status = 'Placed'")['total_placed']
    total_ready = db.fetchone("SELECT COUNT(*) as total_ready FROM placements WHERE placement_status = 'Ready'")['total_ready']

    total_not_placed = total_students - total_placed
    total_not_ready = total_students - total_placed - total_ready

    # Display metrics in horizontal layout
    col1, col2, col3 = st.columns(3)
    col1.metric("🎓 Total Students", total_students)
    col2.metric("🎉 Total Placed", total_placed)
    col3.metric("📋 Not Placed", total_not_placed)

    st.divider()

    # Display Ready and Not Ready
    col4, col5 = st.columns(2)
    col4.metric("🟢 Ready", total_ready)
    col5.metric("🔴 Not Ready", total_not_ready)

    st.divider()

    # Placed Students by Course
    course = st.selectbox("🎯 Filter Placed Students by Course", get_courses())
    placed_query = '''
        SELECT s.student_id, s.name, s.email, s.phone, pl.company_name, pl.placement_package
        FROM students s
        JOIN placements pl ON s.student_id = pl.student_id
        WHERE pl.placement_status = 'Placed' AND s.course_batch = %s
    '''
    placed_students = pd.DataFrame(db.fetchall(placed_query, (course,)))

    if not placed_students.empty:
        st.subheader("✅ Placed Students")
        st.dataframe(placed_students, use_container_width=True)
    else:
        st.info("No students placed for the selected course.")

    st.divider()

    # Ready Students by Course
    ready_course = st.selectbox("📌 Filter Ready Students by Course", get_courses())
    ready_query = '''
        SELECT s.student_id, s.name, s.email, s.phone
        FROM students s
        JOIN placements pl ON s.student_id = pl.student_id
        WHERE pl.placement_status = 'Ready' AND s.course_batch = %s
    '''
    ready_students = pd.DataFrame(db.fetchall(ready_query, (ready_course,)))

    if not ready_students.empty:
        st.subheader("🟢 Ready Students")
        st.dataframe(ready_students, use_container_width=True)
    else:
        st.info("No students in Ready state for the selected course.")

    db.close()

# ----------------------------- MENU 2: FILTER BY CRITERIA -----------------------------
def show_criteria_dashboard():
    st.header("🎯 Filter by Criteria")

    # Course selection dropdown
    course = st.selectbox("Select Course", get_courses())

    # CodeKata input (with range validation)
    codekata = st.number_input("CodeKata Problems Solved (📌Minimum 250 CodeKata problems solved)", min_value=1, max_value=600, value=150)
    if codekata < 1 or codekata > 600:
        st.warning("⚠️ CodeKata problems must be between 1 and 600")

    # Mini Projects slider
    projects = st.slider("Mini Projects Done (📌Atleast 8 Mini Projects completed)", min_value=1, max_value=10, value=5)

    # Soft Skills input (average of 6 metrics)
    softskills_min = st.number_input("Soft Skills Score (📌Average Soft Skills score above 70)", min_value=1, max_value=100, value=60)
    if softskills_min < 1 or softskills_min > 100:
        st.warning("⚠️ Soft skills score must be between 1 and 100")

    # Button click triggers filter
    if st.button("🔍 Filter the Students"):
        db = DatabaseConnection()

        # SQL Query with >= for mini projects and soft skills
        query = '''
            SELECT s.student_id, s.name, s.email, s.phone, s.course_batch,
                   p.language, p.problems_solved, p.mini_projects,
                   ss.communication, ss.teamwork, ss.presentation, ss.leadership,
                   ss.critical_thinking, ss.interpersonal_skills,
                   ROUND((ss.communication + ss.teamwork + ss.presentation + ss.leadership +
                          ss.critical_thinking + ss.interpersonal_skills) / 6.0, 2) AS soft_skill_avg,
                   pl.placement_status
            FROM students s
            JOIN programming p ON s.student_id = p.student_id
            JOIN soft_skills ss ON s.student_id = ss.student_id
            JOIN placements pl ON s.student_id = pl.student_id
            WHERE s.course_batch = %s
              AND p.problems_solved >= %s
              AND p.mini_projects >= %s
              AND ROUND((ss.communication + ss.teamwork + ss.presentation + ss.leadership +
                         ss.critical_thinking + ss.interpersonal_skills) / 6.0, 2) >= %s
              AND pl.placement_status != 'Placed'
        '''

        # Run query with inputs
        filtered_students = pd.DataFrame(
            db.fetchall(query, (course, codekata, projects, softskills_min))
        )

        # Display results
        if not filtered_students.empty:
            st.subheader("✅ Filtered Students")
            st.dataframe(filtered_students, use_container_width=True)
        else:
            st.info("🔍 No students matched the given criteria.")
        db.close()


# ----------------------------- get_courses FUNCTION -----------------------------
def get_courses():
    return [
        "Data Science", "Full Stack Development", "Automation & Testing",
        "UI/UX", "DevOps", "Data Engineering", "Business Analytics with Digital Marketing"
    ]

# ----------------------------- MENU 3: INSIGHTS -----------------------------
def show_insights():
    st.header("📊 Insights from SQL Queries")
    options = {
        "Top 5 students ready for placement": '''
            SELECT s.student_id, s.name, s.course_batch,
                   ROUND((ss.communication + ss.teamwork + ss.presentation + ss.leadership +
                          ss.critical_thinking + ss.interpersonal_skills)/6, 2) as soft_skill_avg,
                   p.problems_solved
            FROM students s
            JOIN soft_skills ss ON s.student_id = ss.student_id
            JOIN programming p ON s.student_id = p.student_id
            JOIN placements pl ON s.student_id = pl.student_id
            WHERE pl.placement_status = 'Ready'
            ORDER BY soft_skill_avg DESC, p.problems_solved DESC
            LIMIT 5
        ''',
        "Distribution of soft skills scores": '''
            SELECT s.student_id, s.name, ss.communication, ss.teamwork, ss.presentation, ss.leadership, ss.critical_thinking, ss.interpersonal_skills
            FROM students s
            JOIN soft_skills ss ON s.student_id = ss.student_id
        ''',
        "Top 20 performing students in mock interview": '''
            SELECT s.student_id, s.name, pl.mock_interview_score
            FROM students s
            JOIN placements pl ON s.student_id = pl.student_id
            ORDER BY pl.mock_interview_score DESC
            LIMIT 20
        ''',
        "Top 10 students with highest package": '''
            SELECT s.student_id, s.name, pl.company_name, pl.placement_package
            FROM students s
            JOIN placements pl ON s.student_id = pl.student_id
            WHERE pl.placement_status = 'Placed'
            ORDER BY pl.placement_package DESC
            LIMIT 10
        ''',
        "Students with more than 4 certificates": '''
            SELECT s.student_id, s.name, p.certifications_earned
            FROM students s
            JOIN programming p ON s.student_id = p.student_id
            WHERE p.certifications_earned > 4
        ''',
        "Join all student tables": '''
            SELECT s.student_id, s.name, s.email, s.course_batch,
                   p.language, p.problems_solved, p.certifications_earned,
                   ss.communication, ss.teamwork, ss.presentation,
                   ss.leadership, ss.critical_thinking, ss.interpersonal_skills,
                   pl.placement_status, pl.company_name, pl.placement_package
            FROM students s
            JOIN programming p ON s.student_id = p.student_id
            JOIN soft_skills ss ON s.student_id = ss.student_id
            JOIN placements pl ON s.student_id = pl.student_id
        ''',
        "Top mini project performers": '''
            SELECT s.student_id, s.name, p.mini_projects
            FROM students s
            JOIN programming p ON s.student_id = p.student_id
            WHERE p.mini_projects IN (9, 10)
        ''',
        "Students graduating this year": '''
            SELECT student_id, name, graduation_year
            FROM students
            WHERE graduation_year = YEAR(CURDATE())
        ''',
        "Students with more than 2 internships": '''
            SELECT s.student_id, s.name, pl.internships_completed
            FROM students s
            JOIN placements pl ON s.student_id = pl.student_id
            WHERE pl.internships_completed > 2
        ''',
        "Average programming performance per batch": '''
            SELECT s.course_batch, ROUND(AVG(p.problems_solved), 2) AS avg_problems
            FROM students s JOIN programming p ON s.student_id = p.student_id
            GROUP BY s.course_batch
        '''
    }

    selected_query = st.selectbox("📌 Choose an insight to explore", list(options.keys()))
    db = DatabaseConnection()
    df = pd.DataFrame(db.fetchall(options[selected_query]))
    st.dataframe(df, use_container_width=True)
    db.close()

# ----------------------------- MAIN APP -----------------------------
def main():
    st.set_page_config(page_title="Placement Eligibility App", layout="wide")
    st.sidebar.title("📚 Placement App Menu")
    menu = st.sidebar.radio("Navigate", ("Overview", "Filter by Criteria", "Insights"))

    if menu == "Overview":
        show_overview()
    elif menu == "Filter by Criteria":
        show_criteria_dashboard()
    elif menu == "Insights":
        show_insights()

if __name__ == '__main__':
    main()
