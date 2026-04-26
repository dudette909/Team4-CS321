from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:8000"


def test_game_navigation():

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # ---- LOGIN ----
        page.goto(f"{BASE_URL}/login/")
        page.fill("input[name='username']", "testuser1")
        page.fill("input[name='password']", "TestPass123!")
        page.click("button[type='submit']")

        page.wait_for_url("**/dashboard/")
        print("Login successful")

        games = [
            ("Hangman", "/hangman/"),
            ("TicTacToe", "/tictactoe/"),
            ("MindMosaic", "/mindmosaic/"),
        ]

        for game_name, game_url in games:

            page.goto(f"{BASE_URL}/dashboard/")
            page.wait_for_load_state("networkidle")

            page.locator(f"a[href='{game_url}']").click()

            page.wait_for_url(f"**{game_url}")
            assert game_url in page.url.lower()

            print(f"{game_name} opened successfully")

        browser.close()


if __name__ == "__main__":
    test_game_navigation()
