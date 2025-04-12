import streamlit as st
import pandas as pd
import random

# Sample database simulation
data = {
    'candidates': [
        {'name': 'Alice', 'skills': ['Python', 'Data Analysis'], 'score': 85, 'feedback': []},
        {'name': 'Bob', 'skills': ['JavaScript', 'React'], 'score': 78, 'feedback': []},
        {'name': 'Charlie', 'skills': ['Java', 'Spring'], 'score': 90, 'feedback': []}
    ],
    'jobs': [
        {'title': 'Backend Developer', 'required_skills': ['Python', 'Django'], 'salary': '₹10-12 LPA', 'culture': 'Collaborative', 'work_sample': 'Implement REST API service for orders.'},
        {'title': 'Frontend Developer', 'required_skills': ['JavaScript', 'React'], 'salary': '₹8-10 LPA', 'culture': 'Creative', 'work_sample': 'Design interactive UI for the dashboard.'},
        {'title': 'Data Analyst', 'required_skills': ['Python', 'Data Analysis'], 'salary': '₹9-11 LPA', 'culture': 'Analytical', 'work_sample': 'Analyze customer retention datasets.'}
    ],
    'interview_status': []
}

# Sample quiz questions for knowledge check
def get_quiz_questions():
    return {
        'Python': [
            {"question": "What is the correct syntax to output 'Hello World' in Python?", "options": ["echo 'Hello World'", "print('Hello World')", "console.log('Hello World')", "printf('Hello World')"], "answer": "print('Hello World')"},
            {"question": "Which function is used to get the length of a list?", "options": ["len()", "length()", "size()", "count()"], "answer": "len()"}
        ],
        'JavaScript': [
            {"question": "Which of the following is the correct way to define a function in JavaScript?", "options": ["function myFunction()", "def myFunction()", "myFunction() = function", "func myFunction()"], "answer": "function myFunction()"},
            {"question": "Which operator is used to compare both value and type in JavaScript?", "options": ["==", "===", "=", "!="], "answer": "==="}
        ]
    }

# User Login
def login():
    st.set_page_config(page_title="Anti-Resume Job Platform", layout="wide")
    st.title("🔐 Welcome to Anti-Resume Hiring Platform")
    st.write("Please select your role and log in.")

    role = st.radio("Role:", ["Candidate", "Recruiter", "Interviewer"], horizontal=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login")

    if login_btn:
        if username and password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["role"] = role
            st.success(f"Logged in as {role}: {username}")
            st.experimental_rerun()
        else:
            st.error("Please enter both username and password.")

# Candidate Portal
def candidate_portal():
    st.title(f"🧑‍💻 Candidate Dashboard")
    st.header("Submit Your Challenge Result")

    with st.form("submit_challenge"):
        skills = st.text_input("Your Skills (comma-separated)")
        score = st.slider("Challenge Score", 0, 100, 70)
        submit = st.form_submit_button("Submit")

    if submit:
        data['candidates'].append({
            'name': st.session_state['username'],
            'skills': [s.strip() for s in skills.split(',')],
            'score': score,
            'feedback': []
        })
        st.success("✅ Challenge result submitted!")

    st.subheader("🧠 Take Knowledge Quiz")
    quiz_bank = get_quiz_questions()
    selected_skill = st.selectbox("Choose a Quiz Topic", list(quiz_bank.keys()))

    if selected_skill:
        question = random.choice(quiz_bank[selected_skill])
        st.write(question['question'])
        answer = st.radio("Select your answer:", question['options'])
        if st.button("Submit Answer"):
            if answer == question['answer']:
                st.success("Correct! Well done.")
            else:
                st.error(f"Incorrect. The correct answer is: {question['answer']}")

    st.subheader("📋 Your Feedback History")
    for c in data['candidates']:
        if c['name'] == st.session_state['username'] and c['feedback']:
            for fb in c['feedback']:
                st.info(f"💬 {fb}")

# Recruiter Portal
def recruiter_portal():
    st.title(f"🏢 Recruiter Dashboard")
    st.header("Post a New Job")

    with st.form("job_form"):
        title = st.text_input("Job Title")
        required_skills = st.text_input("Required Skills (comma-separated)")
        salary = st.text_input("Salary Range")
        culture = st.text_input("Company Culture")
        work_sample = st.text_area("Describe a Work Sample Task")
        submit = st.form_submit_button("Post Job")

    if submit:
        data['jobs'].append({
            'title': title,
            'required_skills': [s.strip() for s in required_skills.split(',')],
            'salary': salary,
            'culture': culture,
            'work_sample': work_sample
        })
        st.success("✅ Job posted successfully!")

    st.header("🤝 Blind Match Candidates to Jobs")
    matches = []
    for candidate in data['candidates']:
        for job in data['jobs']:
            match_score = min(100, len(set(candidate['skills']) & set(job['required_skills'])) * 20 + candidate['score'])
            matches.append({
                'Candidate': candidate['name'],
                'Job Title': job['title'],
                'Match Score': match_score,
                'Salary': job['salary'],
                'Culture Fit': job['culture']
            })

    st.dataframe(pd.DataFrame(matches).sort_values(by="Match Score", ascending=False).reset_index(drop=True))

    st.header("📬 Post-Hire Feedback")
    candidate_names = [c['name'] for c in data['candidates']]
    selected = st.selectbox("Select Candidate", candidate_names)
    feedback = st.text_area("Leave Feedback")
    if st.button("Submit Feedback"):
        for c in data['candidates']:
            if c['name'] == selected:
                c['feedback'].append(feedback)
                st.success("✅ Feedback submitted!")

# Interviewer Portal
def interviewer_portal():
    st.title("👔 Interviewer Dashboard")
    st.header("Schedule & Track Interviews")

    candidates_list = [c['name'] for c in data['candidates']]
    candidate = st.selectbox("Select Candidate for Interview", candidates_list)
    status = st.selectbox("Interview Status", ["Scheduled", "Completed", "Rejected", "Selected"])

    if st.button("Update Interview Status"):
        data['interview_status'].append({'candidate': candidate, 'status': status})
        st.success(f"✅ Status updated for {candidate}!")

    st.subheader("📊 Interview Progress")
    if data['interview_status']:
        st.dataframe(pd.DataFrame(data['interview_status']))

# Main App Logic
def main():
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        login()
    else:
        if st.session_state['role'] == "Candidate":
            candidate_portal()
        elif st.session_state['role'] == "Recruiter":
            recruiter_portal()
        elif st.session_state['role'] == "Interviewer":
            interviewer_portal()

if __name__ == "__main__":
    main()
