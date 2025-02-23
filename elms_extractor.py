import requests
from bs4 import BeautifulSoup
import re
import csv
import json
def extract_csrf_token(html):
    soup = BeautifulSoup(html, "html.parser")
    token_input = soup.find("input", {"name": "logintoken"})
    return token_input["value"] if token_input else None
def extract_session_key(html):
    soup = BeautifulSoup(html, "html.parser")
    token_input = soup.find('input', {'name': 'sesskey'})
    return token_input["value"] if token_input else None
def login():
    session = requests.Session()
    login_page = session.get("https://elms.uiu.ac.bd/login/index.php")  # Get login page
    
    csrf_token = extract_csrf_token(login_page.text)  # Extract
    if csrf_token:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        payload = {
            "username": username,
            "password": password,
            "logintoken": csrf_token
        }
        response = session.post("https://elms.uiu.ac.bd/login/index.php", data=payload)
        if "Dashboard" in response.text:  # Adjust this condition as needed
            print("Login successful!")
            session_key = extract_session_key(response.text)
            return session , session_key
        else:
            print("Login failed.")
            return None
    else:
        print("Failed to extract CSRF token.")
        return None

def get_all_course_id(session,session_key):
    course_url = "https://elms.uiu.ac.bd/lib/ajax/service.php?sesskey="+session_key+"&info=core_course_get_enrolled_courses_by_timeline_classification"
    data = [
        {
            "index": 0,
            "methodname": "core_course_get_enrolled_courses_by_timeline_classification",
            "args": {
                "offset": 0,
                "limit": 24,
                "classification": "all",
                "sort": "fullname",
                "customfieldname": "",
                "customfieldvalue": "",
                "requiredfields": [
                    "id",
                    "fullname",
                    "shortname",
                    "showcoursecategory",
                    "showshortname",
                    "visible",
                    "enddate"
                ]
            }
        }
    ]
    all_course = session.post(course_url,json=data)
    #course_soup = BeautifulSoup(all_course.text, "html.parser")
    json_data = json.loads(all_course.text)
    json_data[0]['data']['courses'][0]['id']
    all_course_details = [course_details for course_details in json_data[0]['data']['courses']]
    all_course_id = [course['id'] for course in all_course_details]
    return all_course_id

def extractAllCourseWithName(session, session_key):
    course_url = "https://elms.uiu.ac.bd/lib/ajax/service.php?sesskey="+session_key+"&info=core_course_get_enrolled_courses_by_timeline_classification"
    data = [
        {
            "index": 0,
            "methodname": "core_course_get_enrolled_courses_by_timeline_classification",
            "args": {
                "offset": 0,
                "limit": 24,
                "classification": "all",
                "sort": "fullname",
                "customfieldname": "",
                "customfieldvalue": "",
                "requiredfields": [
                    "id",
                    "fullname",
                    "shortname",
                    "showcoursecategory",
                    "showshortname",
                    "visible",
                    "enddate"
                ]
            }
        }
    ]
    all_course = session.post(course_url,json=data)
    #course_soup = BeautifulSoup(all_course.text, "html.parser")
    json_data = json.loads(all_course.text)
    json_data[0]['data']['courses'][0]['id']
    all_course_details = [course_details for course_details in json_data[0]['data']['courses']]
    course_name_id = {
    course['fullname'].split(":", 1)[-1].strip(): course['id']
    for course in all_course_details
    }
    return course_name_id

def extract_course_by_id(session,course_id):
    full_list_url = "https://elms.uiu.ac.bd/user/index.php?page=0&perpage=5000&contextid=0&id="+course_id+"&newcourse"
    response = session.get(full_list_url)
    soup = BeautifulSoup(response.text, "html.parser")
    coursename = soup.find_all('h1')
    course_name = coursename[0].text.strip()
    print(f"Extracting data for course: {course_name}")
    course_code = re.search(r'(Spring|Fall|Summer)\s\d{2,4}\s([^:]+)', course_name)
    course_code = course_code.group(2).strip().replace(" ", "_")
    course_code = course_code.replace("/", "_")
    # Extract all profile links
    profile_links = [a["href"] for a in soup.find_all("a", class_="d-inline-block aabtn", href=True)]
    profile_links = list(set(profile_links))  # Remove duplicates

    emails = []
    users_data = []

    for profile_url in profile_links:
        profile_page = session.get(profile_url)
        profile_soup = BeautifulSoup(profile_page.text, "html.parser")
        profile_details = profile_soup.find_all('div', class_="card card-body card-profile")

        if profile_details:
            name = profile_details[0].find('h3').text.strip()  
            email_li = profile_soup.find('li', class_='contentnode')

            if email_li:
                email_tag = email_li.find('a', href=True)
                email = email_tag.text.strip() if email_tag else None
                if email:
                    emails.append(email)
                    users_data.append((name, email))
                    print(f"Name: {name}, Email: {email}")

    print("\nTotal Emails Found:", len(emails))

    # Save to CSV file
    csv_filename = course_code+"_"+"users.csv"
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Email"])  # Header
        writer.writerows(users_data)  # Data

    print(f"CSV file '{csv_filename}' saved successfully.")

    # Save only emails to a text file
    email_filename = course_code+"_"+"emails.txt"
    with open(email_filename, mode="w", encoding="utf-8") as file:
        for email in emails:
            file.write(email + "\n")

    print(f"Email list file '{email_filename}' saved successfully.")


if __name__ == "__main__":
    session , session_key = login()
    
    if session_key is None:
        print("Failed to Login Properly.")
        print("Exiting program.")
        exit()
    option = """Choose your option:
    1. Extract all courses
    2. Extract Course By ID
    3. Show All Course ID with Name
    4. Exit"""
    while True:
        print(option)
        choice = input("Enter your choice: ")
        if choice == "1":
           course_ids = get_all_course_id(session,session_key)
           print("Please wait. Extracting data...")
           for course_id in course_ids:
            extract_course_by_id(session,str(course_id))
        elif choice == "2":
            course_id = input("Enter Course ID: ")
            print("Please wait. Extracting data...")
            extract_course_by_id(session,course_id)
        elif choice == "3":
            print(extractAllCourseWithName(session, session_key))
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")
            
    print("Thank you for using our service.")
    session.close()