#data_insertion.py
import mysql.connector  # MySQL database connector for Python
from faker import Faker  # Library to generate fake data
import random  # To generate random values

# Initialize Faker with Indian locale for realistic data
faker = Faker('en_IN')

# Mysql DB configuration 
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Mysql@4321',
    'database': 'placement_db'
}

class PlacementDataGenerator:
    """
    Class responsible for generating and inserting synthetic student placement-related data 
    into a MySQL database, including programming skills, soft skills, and placement details.
    """

    def __init__(self, db_config):
        # Establish connection to MySQL database
        self.conn = mysql.connector.connect(**db_config)
        self.cur = self.conn.cursor()

        # Use the pre-initialized Faker object
        self.faker = faker

        # Counters to generate unique IDs
        self.placement_counter = 4001
        self.programming_counter = 4001
        self.soft_skill_counter = 4001

    def create_tables(self):
        """
        Creates the database tables after dropping existing ones, 
        including students, programming, soft_skills, and placements.
        """

        # Temporarily disable foreign key checks for dropping tables
        self.cur.execute("SET FOREIGN_KEY_CHECKS = 0;")

        # Drop tables in reverse dependency order to avoid constraint errors
        # self.cur.execute("DROP TABLE IF EXISTS placements")
        # self.cur.execute("DROP TABLE IF EXISTS programming")
        # self.cur.execute("DROP TABLE IF EXISTS soft_skills")
        # self.cur.execute("DROP TABLE IF EXISTS students")

        #Using If NOT EXISTS to avoid constraint errors
        # Create the students table
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                age INT,
                gender VARCHAR(10),
                email VARCHAR(100),
                phone VARCHAR(20),
                enrollment_year INT,
                course_batch VARCHAR(100),
                city VARCHAR(100),
                graduation_year INT
            )
        """)

        # Create the programming skills table
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS programming (
                programming_id VARCHAR(20) PRIMARY KEY,
                student_id INT,
                language VARCHAR(100),
                problems_solved INT,
                assessments_completed INT,
                mini_projects INT,
                certifications_earned INT,
                latest_project_score INT,
                FOREIGN KEY (student_id) REFERENCES students(student_id)
            )
        """)

        # Create the soft skills table
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS soft_skills (
                soft_skill_id VARCHAR(20) PRIMARY KEY,
                student_id INT,
                communication INT,
                teamwork INT,
                presentation INT,
                leadership INT,
                critical_thinking INT,
                interpersonal_skills INT,
                FOREIGN KEY (student_id) REFERENCES students(student_id)
            )
        """)

        # Create the placements table
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS placements (
                placement_id VARCHAR(20) PRIMARY KEY,
                student_id INT,
                mock_interview_score INT,
                internships_completed INT,
                placement_status VARCHAR(20),
                company_name VARCHAR(100),
                placement_package VARCHAR(40),
                interview_rounds_cleared INT,
                placement_date DATE,
                FOREIGN KEY (student_id) REFERENCES students(student_id)
            )
        """)

        # Commit table creation
        self.conn.commit()

    def get_languages_for_course(self, course):
        """
        Returns a string of randomly selected programming languages/tools 
        relevant to the provided course name.
        """
        mapping = {
            'Data Science': ['Python', 'SQL'],
            'Full Stack Development': ['JavaScript', 'Node.js', 'React', 'HTML', 'CSS'],
            'Automation & Testing': ['Python', 'Selenium', 'Java'],
            'UI/UX': ['HTML', 'CSS', 'Figma'],
            'DevOps': ['Shell', 'Python', 'Docker', 'Kubernetes'],
            'Data Engineering': ['Python', 'SQL', 'Spark'],
            'Business Analytics with Digital Marketing': ['Excel', 'SQL', 'Python']
        }

        # Randomly sample 1 to all tools/languages for a course
        return ', '.join(random.sample(mapping[course], k=random.randint(1, len(mapping[course]))))

    def generate_ids(self, name, enrollment_year):
        """
        Generate unique custom IDs for placement, programming, and soft skills
        based on the student name and enrollment year.
        """
        name_parts = name.split()
        first = name_parts[0][0].upper()
        second = name_parts[1][0].upper() if len(name_parts) > 1 else 'X'
        year_suffix = str(enrollment_year)[-2:]

        placement_id = f"{first}{second}{year_suffix}{self.placement_counter}"
        programming_id = f"{second}{first}{self.programming_counter}"
        soft_skill_id = f"{first}{second}{self.soft_skill_counter}"

        # Increment counters for next student
        self.placement_counter += 1
        self.programming_counter += 1
        self.soft_skill_counter += 1

        return placement_id, programming_id, soft_skill_id

    def populate_data(self, total_students=1000):
        """
        Populates the database with randomly generated synthetic data 
        for the given number of students.
        """
        # Available course list
        courses = [
            'Data Science', 'Full Stack Development', 'Automation & Testing',
            'UI/UX', 'DevOps', 'Data Engineering', 'Business Analytics with Digital Marketing'
        ]

        for _ in range(total_students):
            # Generate student profile
            name = self.faker.name()
            age = random.randint(20, 35)
            gender = random.choice(['Male', 'Female'])
            email = self.faker.email()
            phone = self.faker.phone_number()
            enrollment_year = random.randint(2022, 2025)
            course_batch = random.choice(courses)
            city = self.faker.city()
            graduation_year = enrollment_year

            # Insert student into students table
            self.cur.execute("""
                INSERT INTO students (name, age, gender, email, phone, enrollment_year, course_batch, city, graduation_year)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (name, age, gender, email, phone, enrollment_year, course_batch, city, graduation_year))
            student_id = self.cur.lastrowid

            # Generate IDs and programming languages based on course
            placement_id, programming_id, soft_skill_id = self.generate_ids(name, enrollment_year)
            language = self.get_languages_for_course(course_batch)

            # Decide placement status and generate attributes accordingly
            rand_val = random.random()
            if rand_val < 0.15:  # ~15% get placed
                placement_status = 'Placed'
                problems_solved = random.randint(250, 600)
                mock_score = random.randint(70, 100)
                soft_skills = [random.randint(70, 100) for _ in range(6)]
                company_name = self.faker.company()
                placement_package = f"{round(random.uniform(3.5, 15), 2)} LPA"
                interview_rounds = random.randint(3, 5)
                placement_date = self.faker.date_this_decade()
                internships = random.randint(1, 3)
            elif rand_val < 0.53:  # ~38% are ready
                placement_status = 'Ready'
                problems_solved = random.randint(250, 600)
                mock_score = random.randint(70, 85)
                soft_skills = [random.randint(70, 100) for _ in range(6)]
                company_name = None
                placement_package = None
                interview_rounds = None
                placement_date = None
                internships = random.randint(0, 2)
            else:  # remaining students are Not Ready
                placement_status = 'Not Ready'
                problems_solved = random.randint(50, 249)
                mock_score = random.randint(50, 69)
                soft_skills = [random.randint(50, 69) for _ in range(6)]
                company_name = None
                placement_package = None
                interview_rounds = None
                placement_date = None
                internships = random.randint(0, 1)

            # Insert into programming table
            mini_projects = random.randint(8, 10) if placement_status in ['Placed', 'Ready'] else random.randint(5, 7)
            self.cur.execute("""
                INSERT INTO programming (programming_id, student_id, language, problems_solved, assessments_completed,
                    mini_projects, certifications_earned, latest_project_score)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                programming_id, student_id, language, problems_solved,
                random.randint(0, 10), mini_projects,
                random.randint(0, 5), random.randint(60, 100)
            ))

            # Insert into soft_skills table
            self.cur.execute("""
                INSERT INTO soft_skills (soft_skill_id, student_id, communication, teamwork, presentation,
                    leadership, critical_thinking, interpersonal_skills)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (soft_skill_id, student_id, *soft_skills))

            # Insert into placements table
            self.cur.execute("""
                INSERT INTO placements (placement_id, student_id, mock_interview_score, internships_completed,
                    placement_status, company_name, placement_package, interview_rounds_cleared, placement_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                placement_id, student_id, mock_score, internships,
                placement_status, company_name, placement_package,
                interview_rounds, placement_date
            ))

        # Final commit to save all inserted records
        self.conn.commit()
        print(f"✅ Successfully inserted {total_students} student records.")

# Main execution block
if __name__ == "__main__":
    # Instantiate data generator and run table creation and data population
    generator = PlacementDataGenerator(DB_CONFIG)
    generator.create_tables()
    generator.populate_data(total_students=1000)
