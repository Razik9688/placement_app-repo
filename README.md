# placement_app-repo
Placement Eligibility Streamlit Application- Design and implement a Streamlit application where users can input eligibility criteria for placement. Based on these criteria, the application should query a dataset of student information to display eligible candidates' details.


# 🎓 Placement Eligibility Streamlit App

This is a simple and user-friendly web application that helps placement coordinators to check which students are **ready for placement** based on their performance. The app shows student details, their scores, and who is placed, ready, or not ready — all in a clean dashboard format.

---

## 📌 What Does This App Do?

This app helps you:

- ✅ See how many students are placed or not placed
- 🔍 Find students who are **ready for placement** but not yet placed
- 📊 View detailed reports using built-in buttons
- 📚 Use smart filters like course, programming scores, soft skills, and projects

It’s built for **placement coordinators and mentors** to make the placement process easier and smarter.

---

## 🖥️ How It Works (In Simple Words)

1. 🎯 We first create **fake student data** (like names, scores, and placements) using a tool called **Faker**
2. 💾 This data is saved in a **MySQL database** 
3. 📊 A web app is created using **Streamlit**, which reads the data and shows it in an easy-to-use dashboard
4. 🧠 Users can apply filters, search, and get insights — all with a few clicks

---

## 🛠️ Technologies Used (Don’t Worry If You’re New!)

| Tool/Tech     | Why We Use It |
|---------------|----------------|
| Python        | The language we use to build everything |
| Streamlit     | To create the web app interface |
| MySQL         | To store all student data |
| Faker         | To create sample student data |
| Pandas        | To organize and show the data neatly |
| PyMySQL       | To connect Python with MySQL database |

---

## 📷 What You’ll See

- A **Dashboard** with student stats
- Buttons to see:
  - ✅ Placed students
  - 💡 Ready but not placed students
  - 📚 Course-wise performance
- Filters to check:
  - CodeKata scores
  - Mini projects
  - Soft skills
- Insights like:
  - Who has the best placement score?
  - Who completed the most certifications?
  - Who did internships and mock interviews?

---

## 📂 Files in This Project

```bash
placement_app/
├── placement_app.py        # Main app (Streamlit file)
├── data_insertion.py       # Script to insert fake data into MySQL

