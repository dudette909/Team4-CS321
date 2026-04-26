from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:8000"


def test_signup_and_login():

    # Create test users for login scenarios with different combinations of valid and invalid credentials
    test_users = {
        "valid": {
            "username": "testuser1",
            "password": "TestPass123!",
            "able_to_login": True,
        },
        "wrong_user": {
            "username": "wronguser",
            "password": "TestPass123!",
            "able_to_login": False,
        },
        "wrong_password": {
            "username": "testuser1",
            "password": "WrongPass123!",
            "able_to_login": False,
        },
        "wrong_both": {
            "username": "wronguser",
            "password": "WrongPass123!",
            "able_to_login": False,
        },
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        # Signup with valid test user
        page = browser.new_page()
        page.goto(f"{BASE_URL}/register/")
        page.wait_for_selector("input[name='username']")

        page.fill("input[name='username']", test_users["valid"]["username"])
        page.fill("input[name='email']", "testuser1@test.com")
        page.fill("input[name='password1']", test_users["valid"]["password"])
        page.fill("input[name='password2']", test_users["valid"]["password"])

        page.click("button[type='submit']")
        page.wait_for_timeout(1000)

        print("Signup Done")

        page.close()

        # Login tests for all users
        for case in test_users:

            page = browser.new_page()
            page.goto(f"{BASE_URL}/login/")
            page.wait_for_selector("input[name='username']")

            user = test_users[case]["username"]
            pwd = test_users[case]["password"]
            able_to_login = test_users[case]["able_to_login"]

            page.fill("input[name='username']", user)
            page.fill("input[name='password']", pwd)
            page.click("button[type='submit']")

            # If valid user is redirected to dashboard, test passes
            if able_to_login:
                page.wait_for_url("**/dashboard/")
                assert "dashboard" in page.url.lower()
                print(f"PASS: {case}")

            else:
                page.wait_for_timeout(1000)
                assert "dashboard" not in page.url.lower()
                print(f"PASS (expected fail): {case}")

            page.close()

        browser.close()


if __name__ == "__main__":
    test_signup_and_login()
