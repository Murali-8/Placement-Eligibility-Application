# write a code to get data of random records using the faker library

import pandas as pd
import faker
import mysql.connector
import random
import streamlit as st
import os
from random import randint
from streamlit_option_menu import option_menu

fake = faker.Faker(['en_IN']) 
base_year = 2022
student_records = [
    {
    'student_id': i+1  ,
    'name': fake.unique.first_name(),
    'age': fake.random_int(19,30),
    'gender': fake.random_element(['Male', 'Female']),
    'email': fake.email(),
    'phone': fake.phone_number(),
    'enrollment_year': base_year + fake.random_int(0, 3),
    'course_batch':fake.random_element(['BATCH_1', 'BATCH_2','BATCH_3','BATCH_4','BATCH_5']), 
    'city': fake.city(),
    'graduation_year': base_year - fake.random_int(0, 5)
    }
    for i in range(500)
]


programming_ids = list(range(1, 501))  
random.shuffle(programming_ids)
programming_table =[
    {
        'programming_id' : programming_ids[i],
        'student_id': i+1,
        'language': fake.random_element(['Python', 'SQL', 'Java', 'C++','C#' ,'R']),
        'problems_solved': fake.random_int(0, 500),
        'assessments_completed': fake.random_int(0, 50),
        'mini_projects': fake.random_int(0, 20),    
        'certifications_earned': fake.random_int(0, 10),
        'latest_project_score': fake.random_int(0, 100)
    }
    for i in range(500)
]
skill_ids = list(range(1, 501))  
random.shuffle(skill_ids)
softskills_table =[
    {
        'soft_skill_id': skill_ids[i],
        'student_id': i+1,
        'communication': fake.random_int(0, 100),
        'teamwork': fake.random_int(0, 100),
        'presentation': fake.random_int(0, 100),
        'leadership': fake.random_int(0, 100),
        'critical_thinking': fake.random_int(0, 100),
        'interpersonal_skills': fake.random_int(0, 100)
        
    }
    for i in range(500)
]

place_ids = list(range(1, 501))  
random.shuffle(place_ids)
rupee_symbol = "₹"  
placement_table =[
    {
        'placement_id': place_ids[i],
        'student_id': i+1,
        'attendance_percentage' : fake.random_int(0,100),
        'mock_interview_score' : fake.random_int(0,100),
        'internships_completed' : fake.random_int(0,3),
        'placement_status' : fake.random_element(['Ready', 'Not Ready', 'Placed']),
        'company_name' : fake.company(),
        'placement_package' : rupee_symbol + " " +str(fake.random_number(digits=6)), 
        'interview_rounds_cleared' : fake.random_int(0,5),
        #'placement_date' :fake.date_between(start_date='-2y', end_date='today')
        
    }
    for i in range(500)
]


Students_table = pd.DataFrame(student_records)
#Students_table.to_csv('../DATA/Students.csv', index=False)
programming_table = pd.DataFrame(programming_table)
#programming_table.to_csv('../DATA/Programming.csv', index=False)
softskills_table = pd.DataFrame(softskills_table)
#softskills_table.to_csv('../DATA/Softskills.csv', index=False)
placement_table = pd.DataFrame(placement_table)
placement_table['placement_date']= placement_table['placement_status'].apply(lambda x: fake.date_between(start_date='-2y', end_date='today')
                                                                              if x == 'Placed' else None)
#placement_table.to_csv('../DATA/Placement.csv', index=False)  


class Database:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

    def connect(self):
        connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password
        )
        cursor = connection.cursor()
        return connection , cursor
    
    def create_table(self, table_name, columns):
        query = "CREATE TABLE IF NOT EXISTS " + table_name + " (" + ", ".join(columns) + ")"
        cursor.execute(query)
        connection.commit()

class Data_updation:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor


    def insert_data(self, table_name, data_frame):
        columns = ", ".join(data_frame.columns)
        placeholders = ", ".join(["%s"] * len(data_frame.columns)) 

        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        data = [tuple(row) for _, row in data_frame.iterrows()]

        self.cursor.executemany(query, data)
        self.connection.commit()
        

db = Database('localhost', "root", "Muraliph@1994")
query = "create database if not exists placement_eligibility_system"
connection , cursor = db.connect()

cursor.execute(query)
query ="use placement_eligibility_system"
cursor.execute(query)
connection.commit()

table_1 =db.create_table('Students_table',['student_id INT PRIMARY KEY', 'name VARCHAR(200)',
                                'age INT','gender VARCHAR(200)', 
                                'email VARCHAR(200)', 'phone VARCHAR(200)', 
                                'enrollment_year INT', 'course_batch VARCHAR(200)',
                                'city VARCHAR(200)', 'graduation_year INT'])


table_2 =db.create_table('programming_table',['programming_id INT PRIMARY KEY', 'student_id INT',
                                'language VARCHAR(200)', 'problems_solved INT',
                                'assessments_completed INT', 'mini_projects INT',
                                'certifications_earned INT', 'latest_project_score INT',
                                'FOREIGN KEY (student_id) REFERENCES Students_table(student_id)'])


table_3 =db.create_table('softskills_table',['soft_skill_id INT PRIMARY KEY', 'student_id INT',
                                'communication INT', 'teamwork INT',
                                'presentation INT', 'leadership INT',
                                'critical_thinking INT', 'interpersonal_skills INT',
                                'FOREIGN KEY (student_id) REFERENCES Students_table(student_id)'])


table_4 =db.create_table('placement_table',['placement_id INT PRIMARY KEY', 'student_id INT',
                                'attendance_percentage INT', 'mock_interview_score INT',
                                'internships_completed INT', 'placement_status VARCHAR(200)',
                                'company_name VARCHAR(200)', 'placement_package VARCHAR(200)',
                                'interview_rounds_cleared INT', 'placement_date DATE',
                                'FOREIGN KEY (student_id) REFERENCES Students_table(student_id)'])


# insert the data frames in the database 



data_updater = Data_updation(connection, cursor)

#data_updater.insert_data('Students_table', Students_table)

#data_updater.insert_data('programming_table', programming_table)
#data_updater.insert_data('softskills_table', softskills_table)
#data_updater.insert_data('placement_table', placement_table)

print("Python code executed successfully and connected to the database.!")










