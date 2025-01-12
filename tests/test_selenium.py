import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException 
from dotenv import load_dotenv
from time import sleep

# Load environment variables
load_dotenv()

# User fixure - 1 student
@pytest.fixture
def user1():
    return  {'username':'bree', 'password':'cheese', 'email': 'bcheese@wpi.edu', 'id': '999999997', 'phone': '9999999979', 'first_name':'bree', 'last_name': 'cheese' }

# User fixure - 2 faculty
@pytest.fixture
def user2():
    return  {'username':'tee', 'password':'cheer', 'email': 'tcheer@wpi.edu', 'id': '000000001', 'phone': '0000000009', 'first_name':'tee', 'last_name': 'cheer'}

courses_served = ['1', '3']  # Course IDs for "Courses Served as SA"
courses_taken = ['2', '4']  # Course IDs for "Courses Taken"

# Course fixture
@pytest.fixture
def course_data():
    return {
        'course_name': 'DS 4432',
        'section_number': '01',
        'term': '2024-A'
    }


@pytest.fixture
def browser():
    """
    Selenium WebDriver fixture for pytest.
    Initializes the browser and yields the driver instance.
    """
    # Get WebDriver path from the .env file
    chrome_driver_path = os.getenv("CHROME_DRIVER_PATH")
    if not chrome_driver_path:
        raise EnvironmentError("CHROME_DRIVER_PATH not set in .env file or is invalid")

    # Setup WebDriver
    service = Service(executable_path=chrome_driver_path)
    options = webdriver.ChromeOptions()
    options.headless = True  # Run in headless mode
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(8)  # Implicit wait for elements

    yield driver

    # Cleanup: Quit the WebDriver
    driver.quit()

def test_register_faculty(browser, user2):
    browser.get('http://127.0.0.1:5000/index')
    # browser.maximize_window()

    reg_fac_btn = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/main/main/div[3]/div[2]/div/div/a"))
    )
    browser.execute_script("arguments[0].scrollIntoView(true);", reg_fac_btn)
    reg_fac_btn.click()
    sleep(2)

    browser.find_element(By.NAME, "username").send_keys(user2['username'])
    browser.find_element(By.NAME, "email").send_keys(user2['email'])
    browser.find_element(By.NAME, "wpi_id").send_keys(user2['id'])
    browser.find_element(By.NAME, "phone_number").send_keys(user2['phone'])
    browser.find_element(By.NAME, "password").send_keys(user2['password'])
    browser.find_element(By.NAME, "confirm_password").send_keys(user2['password']) 
    browser.find_element(By.NAME, "first_name").send_keys(user2['first_name'])
    browser.find_element(By.NAME, "last_name").send_keys(user2['last_name'])
    sleep(2)

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.NAME, "department"))
    )
    department_selection = browser.find_element(By.NAME, "department").click()  # Dropdown or select field
    department_option = browser.find_element(By.XPATH, "/html/body/main/div/div/div/form/div[9]/select/option[2]").click()

    submit_reg_fac_btn = browser.find_element(By.ID, "submit").click()
    sleep(2)
    success_message = browser.find_element(By.XPATH, "/html/body/main/div")
    assert success_message.is_displayed(), "Registration successful! Please log in with your WPI account."
    sleep(2)

def test_register_student(browser, user1):
    browser.get('http://127.0.0.1:5000/index')
    browser.maximize_window()

    reg_fac_btn = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/main/main/div[3]/div[1]/div/div/a"))
    )
    browser.execute_script("arguments[0].scrollIntoView(true);", reg_fac_btn)
    reg_fac_btn.click()
    sleep(2)

    browser.find_element(By.NAME, "username").send_keys(user1['username'])
    browser.find_element(By.NAME, "email").send_keys(user1['email'])
    browser.find_element(By.NAME, "wpi_id").send_keys(user1['id'])
    browser.find_element(By.NAME, "phone_number").send_keys(user1['phone'])
    browser.find_element(By.NAME, "password").send_keys(user1['password'])
    browser.find_element(By.NAME, "confirm_password").send_keys(user1['password']) 
    browser.find_element(By.NAME, "first_name").send_keys(user1['first_name'])
    browser.find_element(By.NAME, "last_name").send_keys(user1['last_name'])


    sleep(2)

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.NAME, "major"))
    )
    major_selection = browser.find_element(By.NAME, "major").click()  # Dropdown or select field
    major_option = browser.find_element(By.XPATH, "/html/body/main/div/div/div/form/div[9]/select/option[2]").click()


    gpa_input = browser.find_element(By.NAME, "gpa")  
    gpa_input.send_keys("3")

    grad_year = browser.find_element(By.NAME, "graduation_year").click()
    grad_year_option = browser.find_element(By.XPATH, '/html/body/main/div/div/div/form/div[11]/select/option[2]').click()

    for course_id in courses_served:
        checkbox = browser.find_element(By.XPATH, f"//input[@name='courses_served' and @value='{course_id}']")
        if not checkbox.is_selected():
            checkbox.click()

    sleep(2)

    for course_id in courses_taken:
        checkbox = browser.find_element(By.XPATH, f"//input[@name='courses_taken' and @value='{course_id}']")
        if not checkbox.is_selected():
            checkbox.click()
    
    sleep(2)

    submit_reg_stu_btn = browser.find_element(By.ID, "submit").click()
    sleep(2)
    success_message = browser.find_element(By.XPATH, "/html/body/main/div")
    assert success_message.is_displayed(), "Registration successful! Please log in with your WPI account."
    sleep(2)

def test_login_form(browser, user1):
    browser.get('http://localhost:5000/login')
    browser.find_element(By.NAME, "username").send_keys(user1['username'])
    sleep(2)
    browser.find_element(By.NAME, "password").send_keys(user1['password'])
    sleep(2)
    btn = browser.find_element(By.XPATH, "/html/body/main/div/div/div/form/button").click()
    sleep(2)
    #verification
    content = browser.page_source
    assert 'Your Courses' in content 
    assert 'Welcome, Instructor' in content

def test_login_form(browser, user2):
    browser.get('http://localhost:5000/login')
    browser.find_element(By.NAME, "username").send_keys(user2['username'])
    sleep(2)
    browser.find_element(By.NAME, "password").send_keys(user2['password'])
    sleep(2)
    btn = browser.find_element(By.XPATH, "/html/body/main/div/div/div/form/button").click()
    sleep(2)
    #verification
    content = browser.page_source
    assert 'Relevant Positions' in content 
    assert 'Student' in content

# def test_view_positions(browser, user1):
#     """
#     Test to verify that the positions table is displayed
#     and contains specific data on the page.
#     """
#     browser.get('http://localhost:5000/login')
#     browser.find_element(By.NAME, "username").send_keys(user1['username'])
#     browser.find_element(By.NAME, "password").send_keys(user1['password'])
#     btn = browser.find_element(By.XPATH, "/html/body/main/div/div/div/form/button").click()

#     # Verify positions table is displayed
#     positions_table = browser.find_element(By.ID, "positions_table")
#     assert positions_table.is_displayed(), "Positions table is not displayed."

#     # Check for specific content (e.g., course name or instructor)
#     course_name = browser.find_element(By.XPATH, "//td[contains(text(), 'CS 1101')]")
#     assert course_name.is_displayed(), "Expected course 'CS 1101' is not listed."


def test_create_course(browser, user2):
    """
    Test to create a new course as a faculty user.
    """
    # Login as a faculty user
    browser.get('http://localhost:5000/login')
    browser.find_element(By.NAME, "username").send_keys(user2['username'])
    browser.find_element(By.NAME, "password").send_keys(user2['password'])
    btn = browser.find_element(By.XPATH, "/html/body/main/div/div/div/form/button").click()

    # Navigate to the course creation page
    browser.get('http://localhost:5000/course/create')  
    sleep(2)

    # Fill in the course details
    course_choices = browser.find_element(By.NAME, "course_choices").click()  
    course_choices_option = browser.find_element(By.XPATH, "/html/body/main/div/div/form/div[1]/div/select/option[5]").click()
    sleep(2)

    section_number = browser.find_element(By.NAME, "section_number")  
    section_number.send_keys("2")
    sleep(2)
    term = browser.find_element(By.NAME, "term").click() 
    term_choices_option = browser.find_element(By.XPATH, "/html/body/main/div/div/form/div[3]/select/option[1]").click()
    sleep(2)
    submit_btn = browser.find_element(By.XPATH, "/html/body/main/div/div/form/div[4]/button").click()
    sleep(2)
   
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/main/div[1]/text()"))
    )

    # Verify the success message
    success_message = browser.find_element(By.XPATH, "/html/body/main/div[1]/text()")
    assert success_message.is_displayed(), "Course DS 4432 is created"


    browser.get("http://localhost:5000/index") 

    # Verify the new course is listed
    new_course = browser.find_element(By.XPATH, "//td[contains(text(), 'CS 3101 - Advanced Algorithms')]")
    assert new_course.is_displayed(), "Newly created course not found in the course list."



def test_create_SAposition(browser, user2):
    """
    Test to create a new sa positions as a faculty user.
    """
    # Login as a faculty user
    browser.get('http://localhost:5000/login')
    browser.find_element(By.NAME, "username").send_keys(user2['username'])
    browser.find_element(By.NAME, "password").send_keys(user2['password'])
    btn = browser.find_element(By.XPATH, "/html/body/main/div/div/div/form/button").click()

    # Navigate to the course creation page
    browser.get('http://localhost:5000/faculty/create') 
    sleep(2)

    course_section = browser.find_element(By.NAME, "course_section").click()  # Dropdown or select field
    course_section_option = browser.find_element(By.XPATH, "/html/body/main/div/div/form/div[1]/select/option[4]").click()

    sa_number = browser.find_element(By.NAME, "number_of_sas")  
    sa_number.send_keys("3")

    gpa = browser.find_element(By.NAME, "min_gpa")  
    gpa.send_keys("3")

    min_grade = browser.find_element(By.NAME, "min_grade").click()  # Dropdown or select field
    min_grade_option = browser.find_element(By.XPATH, "/html/body/main/div/div/form/div[4]/select/option[1]").click()


    browser.find_element(By.NAME, "prior_experience").click()
    submit_pos_btn = browser.find_element(By.XPATH, "/html/body/main/div/div/form/div[6]/button/label").click()
    sleep(2)

    success_message = browser.find_element(By.XPATH, "/html/body/main/div[1]")
    assert success_message.is_displayed(), "SA Position created successfully!"


def test_view_student_application(browser, user2):
    """
    Test to create a view and assign sa positions as a faculty user.
    """
    # Login as a faculty user
    browser.get('http://localhost:5000/login')
    browser.find_element(By.NAME, "username").send_keys(user1['username'])
    browser.find_element(By.NAME, "password").send_keys(user1['password'])
    btn = browser.find_element(By.XPATH, "/html/body/main/div/div/div/form/button").click()

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/main/div[2]/div/div/div/div/div[2]/div/div/a"))
    )
    view_app_btn = browser.find_element(By.XPATH, "/html/body/main/div[2]/div/div/div/div/div[2]/div/div/a")
    browser.execute_script("arguments[0].scrollIntoView(true);", view_app_btn)
    sleep(2)
    view_app_btn.click()
    sleep(2)

    
    assign_app_btn = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/main/div/div/div/table/tbody/tr[1]/td[9]/form/button"))
    )
    browser.execute_script("arguments[0].scrollIntoView(true);", assign_app_btn)
    sleep(2)
    assign_app_btn.click()
    sleep(2)
    
    success_message = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/main/div[1]"))
    )
    assert "Application approved successfully!" in success_message.text, "Success message not displayed as expected."

    
    content = browser.page_source
    assert 'Already Hired' in content, "Expected content 'Already Hired' not found on the page."



def test_apply_sa_apps(browser, user1):
    """
    Test to apply for sa positions as a student user.
    """
    # Login as a student user
    browser.get('http://localhost:5000/login')
    browser.find_element(By.NAME, "username").send_keys(user1['username'])
    browser.find_element(By.NAME, "password").send_keys(user1['password'])
    btn = browser.find_element(By.XPATH, "/html/body/main/div/div/div/form/button").click()
    sleep(2)
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/main/div[2]/div/button"))
    )

    view_other_pos = browser.find_element(By.XPATH, "/html/body/main/div[2]/div/button")
    browser.execute_script("arguments[0].scrollIntoView(true);", view_other_pos)
    sleep(2)
    view_other_pos.click()
    sleep(2)


    apply_btn = browser.find_element(By.XPATH, "/html/body/main/div[2]/div/div/div/div/div[2]/div/div/a")
    browser.execute_script("arguments[0].scrollIntoView(true);", apply_btn)
    sleep(2)
    apply_btn.click()
    sleep(2)

    confirm_app_btn = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "submit"))
    )
    browser.execute_script("arguments[0].scrollIntoView(true);", confirm_app_btn)
    sleep(2)
    confirm_app_btn.click()
    sleep(2)

    success_message = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/main/div[1]"))
    )
    assert "SA Application successful!" in success_message.text, "Success message not displayed as expected."







