import asyncio
from playwright.async_api import async_playwright

async def login_to_aurora(username: str, password: str) -> None:
    async with async_playwright() as p:
        browser = None
        try:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            await page.goto("https://www.prepaidmeters.net/aurora")
            username_input = page.locator("#mobile")
            if await username_input.count() > 0:
                await username_input.fill(username)
            else:
                print("Username input not found")
                return
            password_input = page.locator("#pin")
            if await password_input.count() > 0:
                await password_input.fill(password)
            else:
                print("Password input not found")
                return

            login_button = page.locator("#login_button")
            if await login_button.count() > 0:
                await login_button.click()
            else:
                print("Login button not found")
                return

            # Wait for the logout link to appear to confirm successful login
            logout_link = page.locator("#logout_link")
            try:
                await logout_link.wait_for(timeout=50000)
                print("Login successful and dashboard loaded.")
            except Exception:
                print("Login may have failed or dashboard did not load.")
        except Exception:
            print("Login may have failed or dashboard did not load.")
            print("Code did not complete successfully.")
        else:
            print("Code Ran to completion.")
        finally:
            if browser:
                await browser.close()

if __name__ == "__main__":
    asyncio.run(login_to_aurora("lwazi.radebe", "8765432"))