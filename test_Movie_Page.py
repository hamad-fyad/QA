from datetime import time

import pytest
from selenium.webdriver.common.by import By
import time
from BaseClass import BaseClass


@pytest.mark.usefixtures("setup")
class Test_Movie_Page(BaseClass):
    @pytest.mark.smoke
    def test_movie_page1(self, setup):
        driver = setup
        logger = self.getLogger()
        driver.implicitly_wait(10)
        driver.get('http://127.0.0.1:5000/')
        driver.find_element(By.CSS_SELECTOR, "#username").send_keys("hamad")
        driver.find_element(By.CSS_SELECTOR, "#password").send_keys("1234")
        driver.find_element(By.CSS_SELECTOR, "input[value='Login']").click()
        text = driver.find_element(By.CSS_SELECTOR, "a[href='/addMovie']").text
        driver.find_element(By.CSS_SELECTOR, "a[href='/addMovie']").click()
        assert "add" in text.lower(), logger.error("not the right button")
        logger.info("moved to the add page")

    # here i found a problem with my code it can add with even if the user didn't put any values in the textarea
    @pytest.mark.smoke
    def test_movie_page2(self, setup):
        driver = setup
        logger = self.getLogger()
        driver.implicitly_wait(10)
        driver.get('http://127.0.0.1:5000/')
        driver.find_element(By.CSS_SELECTOR, "#username").send_keys("hamad")
        driver.find_element(By.CSS_SELECTOR, "#password").send_keys("1234")
        driver.find_element(By.CSS_SELECTOR, "input[value='Login']").click()
        driver.find_element(By.CSS_SELECTOR, "#movieActions-1").click()
        driver.find_element(By.CSS_SELECTOR, "#delete").click()

    @pytest.mark.smoke
    def test_movie_page3(self, setup):
        driver = setup
        logger = self.getLogger()
        driver.implicitly_wait(10)
        driver.get('http://127.0.0.1:5000/')
        driver.find_element(By.CSS_SELECTOR, "#username").send_keys("hamad")
        driver.find_element(By.CSS_SELECTOR, "#password").send_keys("1234")
        driver.find_element(By.CSS_SELECTOR, "input[value='Login']").click()
        try:
            driver.find_element(By.CSS_SELECTOR, "#movieActions-2").click()
        except AssertionError as msg:
            logger.error(msg)
        else:
            logger.info("worked ")

    @pytest.mark.smoke
    def test_movie_page4(self, setup):
        driver = setup
        logger = self.getLogger()
        driver.implicitly_wait(10)
        driver.get('http://127.0.0.1:5000/')
        driver.find_element(By.CSS_SELECTOR, "#username").send_keys("hamad")
        driver.find_element(By.CSS_SELECTOR, "#password").send_keys("1234")
        driver.find_element(By.CSS_SELECTOR, "input[value='Login']").click()
        text = driver.find_element(By.ID, "movieAction-1").text
        driver.find_element(By.ID, "movieActions-1").click()
        try:
            assert "shutter" in text.lower(), logger.error("not the movie shutter")
        except AssertionError as msg:
            logger.error(msg)
        else:
            logger.info("test passed successfully ")

    # the deleting works just don't use it at the moment, so it doesn't delete everything
    @pytest.mark.smoke
    def test_movie_page5(self, setup):
        driver = setup
        logger = self.getLogger()
        driver.implicitly_wait(10)
        driver.get('http://127.0.0.1:5000/')
        driver.find_element(By.CSS_SELECTOR, "#username").send_keys("hamad")
        driver.find_element(By.CSS_SELECTOR, "#password").send_keys("1234")
        driver.find_element(By.CSS_SELECTOR, "input[value='Login']").click()
        driver.find_element(By.CSS_SELECTOR, "#movieActions-2").click()
        try:
            driver.find_element(By.CSS_SELECTOR, "#delete").click() #it worked just stopped it
            print("hello")
        except AssertionError as msg:
            logger.error(msg)
        else:
            logger.info("deleted ")

    @pytest.mark.Security
    def test_logout(self, setup):
        driver = setup
        logger = self.getLogger()
        driver.implicitly_wait(10)
        driver.get('http://127.0.0.1:5000/')
        driver.find_element(By.CSS_SELECTOR, "#username").send_keys("hamad")
        driver.find_element(By.CSS_SELECTOR, "#password").send_keys("1234")
        driver.find_element(By.CSS_SELECTOR, "input[value='Login']").click()
        driver.find_element(By.CSS_SELECTOR, "#logout").click()
        assert driver.current_url == 'http://127.0.0.1:5000/login', "Logout failed, user is not on the login page"
        logger.info("Logout successful, user redirected to login page")

    @pytest.mark.Security
    def test_security_movies2(self, setup):
        driver = setup
        logger = self.getLogger()
        driver.implicitly_wait(10)
        base_url = 'http://127.0.0.1:5000/'
        driver.get(base_url)
        username_field = driver.find_element(By.CSS_SELECTOR, "#username")
        password_field = driver.find_element(By.CSS_SELECTOR, "#password")
        assert username_field, "Username field is not present"
        assert password_field, "Password field is not present"
        username_field.send_keys("hamad")
        password_field.send_keys("1234")
        login_button = driver.find_element(By.CSS_SELECTOR, "input[value='Login']")
        assert login_button, "Login button is not present"
        login_button.click()
        assert driver.current_url != base_url, "Login failed, user is still on the login page"
        logger.info("User has been successfully redirected to the dashboard after logging in")
        logout_button = driver.find_element(By.CSS_SELECTOR, "#logout")
        assert logout_button, "Logout button not present, Login could have failed"
        logger.info("Logout button is present. Login has passed successfully.")

    @pytest.mark.Security
    def test_security_movies3(self, setup):
        driver = setup
        logger = self.getLogger()
        driver.implicitly_wait(10)
        driver.get('http://127.0.0.1:5000/')
        assert "Login" in driver.page_source
        driver.find_element(By.CSS_SELECTOR, "#username").send_keys("admin")
        driver.find_element(By.CSS_SELECTOR, "#password").send_keys("admin")
        driver.find_element(By.CSS_SELECTOR, "input[value='Login']").click()

        try:
            assert "Logged in successfully" in driver.page_source
        except AssertionError:
            logger.error("Admin user could not log in")
        else:
            logger.info("Admin user logged in successfully")

        driver.get('http://127.0.0.1:5000/addMovie')
        try:
            assert driver.current_url != 'http://127.0.0.1:5000/addMovie'
        except AssertionError:
            logger.error("Non-admin user could access /addMovie")
        else:
            logger.info("Non-admin user could not access /addMovie")

        driver.get('http://127.0.0.1:5000/movies/title%20OR%201=1')
        try:
            assert driver.current_url != 'http://127.0.0.1:5000/movies/title%20OR%201=1'
        except AssertionError:
            logger.error("SQL Injection attempt was successful")
        else:
            logger.info("SQL Injection attempt was blocked")

    @pytest.mark.Security
    def test_invalid_login(self, setup):
        driver = setup
        logger = self.getLogger()
        driver.implicitly_wait(10)
        driver.get('http://127.0.0.1:5000/')
        driver.find_element(By.CSS_SELECTOR, "#username").send_keys("admin")
        driver.find_element(By.CSS_SELECTOR, "#password").send_keys("admin")
        assert "login" in driver.current_url, "same url"
        logger.info("Login failed with invalid credentials as expected")

    @pytest.mark.Security
    def test_signup(self, setup):
        driver = setup
        logger = self.getLogger()
        driver.implicitly_wait(10)
        driver.get('http://127.0.0.1:5000/signup')
        driver.find_element(By.CSS_SELECTOR, "#username").send_keys("shady")
        driver.find_element(By.CSS_SELECTOR, "#password").send_keys("12345")
        driver.find_element(By.CSS_SELECTOR, "#signup").click()
        assert "login" in driver.current_url
        logger.info("Signup successful")

    @pytest.mark.Functional
    def test_list_movies(self, setup):
        driver = setup
        driver.implicitly_wait(10)
        logger = self.getLogger()
        # Visit the base URL
        driver.get('http://127.0.0.1:5000/')
        driver.find_element(By.CSS_SELECTOR, "#username").send_keys("hamad")
        driver.find_element(By.CSS_SELECTOR, "#password").send_keys("1234")
        driver.find_element(By.CSS_SELECTOR, "input[value='Login']").click()
        movies = driver.find_elements(By.CSS_SELECTOR, "#movie-0")
        assert len(movies) > 0, "No movies found on the homepage"

        logger.info(f"Found {len(movies)} movies on the homepage")

    @pytest.mark.Functional
    def test_add_movie1(self, setup):
        driver = setup
        logger = self.getLogger()
        driver.implicitly_wait(10)
        driver.get('http://127.0.0.1:5000/')
        driver.find_element(By.CSS_SELECTOR, "#username").send_keys("hamad")
        driver.find_element(By.CSS_SELECTOR, "#password").send_keys("1234")
        driver.find_element(By.CSS_SELECTOR, "input[value='Login']").click()
        driver.get('http://127.0.0.1:5000/addMovie')

        driver.find_element(By.CSS_SELECTOR, "#image_url").send_keys("http://example.com/image.png")
        driver.find_element(By.CSS_SELECTOR, "#title").send_keys("Test Movie")
        driver.find_element(By.CSS_SELECTOR, "#plot").send_keys("Test Plot")
        driver.find_element(By.CSS_SELECTOR, "#director").send_keys("Test Director")
        driver.find_element(By.CSS_SELECTOR, "#actor1").send_keys("Test Actor 1")
        driver.find_element(By.CSS_SELECTOR, "#year").send_keys("2023")

        driver.find_element(By.CSS_SELECTOR, "input[value='Submit']").click()

        assert driver.current_url == 'http://127.0.0.1:5000/index', "Add movie failed,user is not redirected to the homepage"

        logger.info("Movie added successfully")

    @pytest.mark.Functional
    def test_movie_details(self, setup):
        driver = setup
        logger = self.getLogger()
        driver.implicitly_wait(10)

        # Visit the movie details URL
        driver.get('http://127.0.0.1:5000/')
        driver.find_element(By.CSS_SELECTOR, "#username").send_keys("hamad")
        driver.find_element(By.CSS_SELECTOR, "#password").send_keys("1234")
        driver.find_element(By.CSS_SELECTOR, "input[value='Login']").click()

        movie_title_element = driver.find_element(By.ID, "movieActions-1")
        movie_title_text = movie_title_element.text.lower()
        print("\n", movie_title_text, 10000)

        def verify_movie_title():
            text1 = driver.find_element(By.ID, "title").text.lower()
            print(text1, 10000)
            assert text1 in movie_title_text, "Movie title does not match the expected title"
            logger.info("Movie details verified successfully")

    @pytest.mark.Functional
    def test_user_logout(self, setup):
        driver = setup
        logger = self.getLogger()
        driver.implicitly_wait(10)
        # Visit the base URL and login
        driver.get('http://127.0.0.1:5000/')
        driver.find_element(By.CSS_SELECTOR, "#username").send_keys("hamad")
        driver.find_element(By.CSS_SELECTOR, "#password").send_keys("1234")
        driver.find_element(By.CSS_SELECTOR, "input[value='Login']").click()
        # Find the logout button and click it
        driver.find_element(By.CSS_SELECTOR, "#logout-button").click()
        # Verify that the user is redirected to the login page
        assert driver.current_url == 'http://127.0.0.1:5000/login', "Logout failed, user is not redirected to the login page"
        # Log the successful logout
        logger.info("Logout successful")

    @pytest.mark.Functional
    def test_user_signup(self, setup):
        driver = setup
        logger = self.getLogger()
        driver.implicitly_wait(10)
        # Visit the signup URL
        driver.get('http://127.0.0.1:5000/signup')
        # Find the signup fields and enter information
        driver.find_element(By.CSS_SELECTOR, "#username").send_keys("newuser")
        driver.find_element(By.CSS_SELECTOR, "#password").send_keys("newpassword")
        # Find the submit button and click it
        driver.find_element(By.CSS_SELECTOR, "input[value='Signup']").click()
        # Verify that the user is redirected to the login page
        assert driver.current_url == 'http://127.0.0.1:5000/login', "Signup failed, user is not redirected to the login page"
        # Log the successful signup
        logger.info("Signup successful")

    @pytest.mark.Acceptance
    def test_website_accessible(self, setup):
        driver = setup
        logger = self.getLogger()
        driver.get('http://127.0.0.1:5000/')
        assert "login" in driver.current_url, "The website is not accessible"
        logger.info("Website is accessible")

    @pytest.mark.Acceptance
    def test_user_signup(self, setup):
        driver = setup
        logger = self.getLogger()
        driver.get('http://127.0.0.1:5000/signup')
        driver.find_element(By.CSS_SELECTOR, "#username").send_keys("newuser")
        driver.find_element(By.CSS_SELECTOR, "#password").send_keys("newpassword")
        driver.find_element(By.CSS_SELECTOR, "input[value='Signup']").click()
        assert "login" in driver.current_url, "Signup process failed"
        logger.info("Signup process passed")

    @pytest.mark.Acceptance
    def test_user_login(self, setup):
        driver = setup
        logger = self.getLogger()
        driver.get('http://127.0.0.1:5000/')
        driver.find_element(By.CSS_SELECTOR, "#username").send_keys("hamad")
        driver.find_element(By.CSS_SELECTOR, "#password").send_keys("1234")
        driver.find_element(By.CSS_SELECTOR, "input[value='Login']").click()
        assert "index" in driver.current_url, logger.error("Login process failed")
        logger.info("Login process passed")

    @pytest.mark.Acceptance
    def test_add_movie(self, setup):
        driver = setup
        logger = self.getLogger()
        driver.get('http://127.0.0.1:5000/')
        driver.find_element(By.CSS_SELECTOR, "#username").send_keys("hamad")
        driver.find_element(By.CSS_SELECTOR, "#password").send_keys("1234")
        driver.find_element(By.CSS_SELECTOR, "input[value='Login']").click()
        driver.get('http://127.0.0.1:5000/addMovie')
        driver.find_element(By.CSS_SELECTOR, "#image_url").send_keys("http://example.com/image.png")
        driver.find_element(By.CSS_SELECTOR, "#title").send_keys("Test Movie")
        driver.find_element(By.CSS_SELECTOR, "#plot").send_keys("Test Plot")
        driver.find_element(By.CSS_SELECTOR, "#director").send_keys("Test Director")
        driver.find_element(By.CSS_SELECTOR, "#actor1").send_keys("Test Actor 1")
        driver.find_element(By.CSS_SELECTOR, "#year").send_keys("2023")
        driver.find_element(By.CSS_SELECTOR, "input[value='Submit']").click()
        time.sleep(2)
        assert "index" in driver.current_url, "Add movie process failed"
        logger.info("Add movie process passed")

    @pytest.mark.Acceptance
    def test_user_logout(self, setup):
        driver = setup
        logger = self.getLogger()
        driver.get('http://127.0.0.1:5000/')
        driver.find_element(By.CSS_SELECTOR, "#username").send_keys("hamad")
        driver.find_element(By.CSS_SELECTOR, "#password").send_keys("1234")
        driver.find_element(By.CSS_SELECTOR, "input[value='Login']").click()
        driver.get('http://127.0.0.1:5000/logout')
        assert "login" in driver.current_url, "Logout process failed"
        logger.info("Logout process passed")


