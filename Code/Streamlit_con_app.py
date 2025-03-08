import streamlit as st
from streamlit_option_menu import option_menu
from App_file import db,data_updater
import pandas as pd


st.set_page_config(layout="wide")
 
with st.sidebar:
    selected = option_menu(
            "Placement App Navigation",
            ["Home", "Eligibility Criteria", "Data Insights","Read Your Data"],
            icons=["house", "person", "bar-chart" ,"building"],
            menu_icon="menu-hamburger",
            default_index=0,
        )

connection , cursor = db.connect() 
query ="use placement_eligibility_system"
cursor.execute(query)
connection.commit()

if selected == "Home":
    st.title("Placement Eligibility Application")
    st.write("Welcome to the Placement Eligibility Application!")
    st.image("/Users/muralidharanv/Documents/GUVI /PROJECTS/PLACEMENT ELIGIBLITY APP/DATA/hr-recruitment-employment-headhunting-artificial-intelligence-ai-robot-hand-pointing-futuristic-human-resources-management-284432425.jpg", width=900)
    st.write("This application is designed to help HR's to select the students for placements based on their skills and eligibility criteria.")
    
  
    with st.form("login_form"):
        username = st.text_input("Username" )
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button(label="Login")
        if submit_button:
            if username == "HR" and password == "ADMIN":
                st.success("Login Successful!")
            else:
                st.error("Invalid Credentials!")


elif selected == "Eligibility Criteria":
    st.title("Eligibility Criteria")
    st.header("Select the Eligibility Criteria for Placement", divider =True)

    st.text("1.Provide the minimum attendance percentage for placement eligibility")

    attendance = st.number_input("Insert a number" ,max_value= 100, min_value=0, key="attendance")
    st.write("The provided number is ", attendance)

    st.text("2.Provide the minimum number of coding problems solved")

    solved_prob_count = st.number_input("Insert a number" ,max_value= 500, min_value=0, key= "solved_prob_count")
    st.write("The provided number is ", solved_prob_count)

    st.text("3.Provide the number of certifications earned")

    certification_count = st.number_input("Insert a number" ,max_value= 10, min_value=0, key = "certifications_count")
    st.write("The provided number is ", certification_count)

    st.text("4.Provide the number of mini projects completed")

    mini_projects_count = st.number_input("Insert a number" ,max_value= 20, min_value=0, key = "mini_projects_count")
    st.write("The provided number is ", mini_projects_count)

    st.text("5.Provide the minimum expected score for final project")

    Final_proj_score= st.slider("Project Score" ,max_value= 100, min_value=0, step= 10,key="Final_proj_score")
    st.write("The provided final project score is ", Final_proj_score)


    

    if st.button("Submit"):
        

        query =  """
            SELECT s.student_id, s.name, p.attendance_percentage, pr.mini_projects,
                pr.problems_solved, pr.certifications_earned, pr.latest_project_score
            FROM Students_table s
            JOIN placement_table p ON s.student_id = p.student_id
            JOIN programming_table pr ON s.student_id = pr.student_id
            JOIN softskills_table sk ON s.student_id = sk.student_id
            WHERE p.attendance_percentage >= %s
            AND pr.problems_solved >= %s
            AND pr.certifications_earned >= %s
            AND pr.mini_projects >= %s
            AND pr.latest_project_score >= %s
            """

        params = (attendance, solved_prob_count,certification_count, mini_projects_count, Final_proj_score)

        cursor.execute(query, params)
        result = cursor.fetchall()
        df = pd.DataFrame(result, columns=['Student ID', 'Name', 'Attendance Percentage', 'Mini Projects',
                                           'Problems Solved', 'Certifications Earned', 'Latest Project Score']) 
        st.dataframe(df)

        if len(result) == 0:
            st.write("No students meet the given criteria")
        else:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(label="📥 Download CSV", data=csv, file_name="filtered_candidates.csv", mime="text/csv")


elif selected == "Data Insights":
    st.title("Data Insights")
    st.header("Insights about the students data", divider =True)

    
    questions = [ "1. Total Number of Students Placed" , "2.  Average Mock Interview Score of Placed and Non-Placed Students",
                 "3. Top 5 Programming Languages Used by Students" , "4. Average Attendance Percentage of Students Who Got Placed",
                 "5. Top 5 students who have solved more number of problems" , "6.Number of Students Who Completed at Least One Internship and Got Placed",
                 "7.Average number of Certifications Earned by Placed and Non-Placed Students" , "8.Top 5 Companies Hiring the Most Students",
                 "9.How Many Students Have Cleared More Than 3 Interview Rounds?", "10.Placement Success based on the problems solved." ]
    selected_question = st.selectbox("Select a question", questions)
    if selected_question == "1. Total Number of Students Placed":
        query = """ SELECT count(*) as total_placed_students 
                    FROM placement_table 
                    WHERE placement_status = 'Placed';"""
        cursor.execute(query)
        result = cursor.fetchone()
        st.write("The total number of students placed is ", result[0])

    elif selected_question == "2.  Average Mock Interview Score of Placed and Non-Placed Students":
        query ="""SELECT placement_status, AVG(mock_interview_score) as avg_mock_score
                  FROM placement_table 
                  GROUP BY placement_status; """ 
        cursor.execute(query)
        result = cursor.fetchall()
        df = pd.DataFrame(result, columns=['Placement Status', 'Average Mock Interview Score'])
        st.write("Average Mock Interview Score of Placed and Non-Placed Students is ", df)
    
    elif selected_question =="3. Top 5 Programming Languages Used by Students":
        query =""" select language, count(*) as student_count
                   from programming_table
                   group by language
                   order by student_count DESC
                   limit 5;"""
        cursor.execute(query)
        result = cursor.fetchall()
        df = pd.DataFrame(result, columns= ['language','student_count'])
        st.write("Top 5 Programming Languages Used by Students is ", df)

    elif selected_question =="4. Average Attendance Percentage of Students Who Got Placed" :
        query = """ select avg(attendance_percentage) as avg_attendance
                from placement_table
                where placement_status = 'Placed';"""
        cursor.execute(query)
        result = cursor.fetchone()
        st.write("Average Attendance Percentage of Students Who Got Placed is ", result[0])

    elif selected_question == "5. Top 5 students who have solved more number of problems":
        query ="""  select s.student_id, s.name, pr.problems_solved
                    from students_table s
                    join programming_table pr on s.student_id = pr.student_id
                    order by pr.problems_solved desc
                    limit 5;"""
        cursor.execute(query)
        result = cursor.fetchall()
        df = pd.DataFrame(result, columns=['Student ID', 'Name', 'Problems Solved'])
        st.write("Top 5 students who have solved more number of problems is ", df)

    elif selected_question =="6.Number of Students Who Completed at Least One Internship and Got Placed":
        query ="""select count(*) as students_with_internships
                from placement_table
                where internships_completed > 0 AND placement_status = 'Placed';"""
        cursor.execute(query)
        result = cursor.fetchone()
        st.write("Number of Students Who Completed at Least One Internship and Got Placed is ", result[0])

    elif selected_question == "7.Average number of Certifications Earned by Placed and Non-Placed Students":
        query = """select placement_status, avg(certifications_earned) as avg_certifications
                from placement_table p
                join programming_table pr on p.student_id = pr.student_id
                group by placement_status;"""
        cursor.execute(query)
        result = cursor.fetchall()
        df = pd.DataFrame(result, columns=['Placement Status', 'Average Certifications'])
        st.write("Average number of Certifications Earned by Placed and Non-Placed Students", df)

    elif selected_question == "8.Top 5 Companies Hiring the Most Students":
        query ="""select company_name, count(*) as student_count
                from placement_table
                where placement_status = 'Placed'
                group by company_name
                order by student_count desc
                limit 5;"""
        cursor.execute(query)
        result = cursor.fetchall()
        df = pd.DataFrame(result, columns=['Company Name', 'Student Count'])
        st.write("Top 5 Companies Hiring the Most Students is ", df)

    elif selected_question == "9.How Many Students Have Cleared More Than 3 Interview Rounds?":
        query = """select count(*) as students_with_more_than_3_rounds
                from placement_table
                where interview_rounds_cleared > 3;
                """    
        cursor.execute(query)
        result = cursor.fetchone()
        st.write("How Many Students Have Cleared More Than 3 Interview Rounds is ", result)

    elif selected_question == "10.Placement Success based on the problems solved.":
        query ="""SELECT 
                    CASE WHEN p.placement_status = 'Placed' THEN 'Placed' ELSE 'Not Placed' END AS placement_status,
                    AVG(pr.problems_solved) AS avg_problems_solved
                FROM programming_table pr
                JOIN placement_table p ON pr.student_id = p.student_id
                GROUP BY placement_status;"""
        cursor.execute(query)
        result = cursor.fetchall()
        df = pd.DataFrame(result, columns=['Placement Status', 'Average Problems Solved'])
        st.write("Placement Success based on the problems solved is ", df)


elif selected == "Read Your Data":

    selected_table = st.radio("Tables", ["Students_table", "programming_table", "softskills_table", "placement_table"])
    st.write("The selected table is",selected_table)

    if st.button("Read"):
        query = f"SELECT * FROM {selected_table}"
        cursor.execute(query)
        result = cursor.fetchall()
        df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])
        st.write(df)
    
    elif st.button("Cancel"):
        st.write("Operation Cancelled")
    
    cursor.close()