import time

from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest
from faker import Faker

fake = Faker()

@pytest.fixture(scope="module")
def setup():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def test_successful_signup(setup):
    setup.get("http://localhost:3000/signup")
    username = fake.user_name()
    email = fake.email()
    phone_number = fake.msisdn()[:11]
    setup.find_element(By.ID, "name").send_keys("test_account")
    setup.find_element(By.ID, "username").send_keys(username)
    setup.find_element(By.ID, "email").send_keys(email)
    setup.find_element(By.ID, "password").send_keys("Password123!")
    setup.find_element(By.ID, "phone_number").send_keys(phone_number)
    setup.find_element(By.ID, "submit").click()
    time.sleep(2)
    alert = setup.switch_to.alert
    alert_message = alert.text
    print(alert_message)  # Print the alert message for debugging purposes
    assert alert_message == "User signed up successfully"
    alert.accept()
    time.sleep(2)
    title = setup.find_element(By.ID, "title")
    assert title.text == "Login"

def test_successful_login(setup):
    setup.get("http://localhost:3000/login")

    setup.find_element(By.ID, "username").send_keys("test_user")
    setup.find_element(By.ID, "password").send_keys("Password123!")
    setup.find_element(By.ID, "submit").click()
    time.sleep(4)
    alert = setup.switch_to.alert
    alert_message = alert.text
    print(alert_message)  # Print the alert message for debugging purposes
    assert alert_message == "User logged in successfully"
    alert.accept()
    time.sleep(2)
    title = setup.find_element(By.ID, "current_user")
    assert title.text == "Logged in as: test_user"
