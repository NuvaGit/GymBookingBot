import tkinter as tk
from tkinter import scrolledtext
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
import time
import threading
import sys

URL = "https://hub.ucd.ie/usis/W_HU_MENU.P_PUBLISH?p_tag=GYMBOOK"
REFRESH_INTERVAL = 1  # Time interval for page refreshes

BACKGROUND_COLOR = "#1E1E2E"
TEXT_COLOR = "#ffffff"
BUTTON_COLOR = "#4CAF50"
STOP_BUTTON_COLOR = "#FF4B4B"
WARNING_COLOR = "#FFD700"
FONT = ("Arial", 14)

driver = None
bot_running = False


class TerminalOutput:
    """Redirects terminal output to the Tkinter UI console."""
    def __init__(self, widget):
        self.widget = widget
        self.widget.config(state=tk.DISABLED)

    def write(self, text):
        self.widget.config(state=tk.NORMAL)
        self.widget.insert(tk.END, text)
        self.widget.see(tk.END)
        self.widget.config(state=tk.DISABLED)

    def flush(self):
        pass


def start_booking(username):
    """Starts the booking process in a separate thread."""
    global bot_running, driver

    if not username:
        warning_label.config(text="⚠ Please enter your UCD username!", fg="red")
        return

    warning_label.config(text="✅ Booking bot is now running!", fg="lightgreen")
    console_output.delete("1.0", tk.END)
    bot_running = True

    def run_bot():
        global driver, bot_running
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")

            driver = webdriver.Chrome(options=options)
            driver.get(URL)
            wait = WebDriverWait(driver, 5)

            while bot_running:
                driver.refresh()
                print("🔄 Page refreshed")
                time.sleep(0.25)

                def accept_cookies():
                    try:
                        cookies_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Accept')]")
                        driver.execute_script("arguments[0].click();", cookies_button)
                        print("✅ Accepted cookies")
                        time.sleep(0.25)
                    except NoSuchElementException:
                        pass  # No cookies popup, continue

                accept_cookies()

                # ✅ Look for available slots (Check for an anchor link before proceeding)
                slots = driver.find_elements(By.XPATH, "//table//tr")
                booking_found = False  # Flag to track if booking was found

                for slot in slots:
                    if not bot_running:
                        return

                    try:
                        book_link = slot.find_element(By.TAG_NAME, "a")  # Look for an anchor tag

                        if book_link.is_displayed() and book_link.is_enabled():
                            print(f"✅ Booking available at {slot.text}. Clicking link...")
                            driver.execute_script("arguments[0].click();", book_link)
                            time.sleep(1)  # Wait for the next page to load
                            booking_found = True  # Mark that we found a booking
                            break  # Exit the loop if a booking was found
                    except NoSuchElementException:
                        pass  # No anchor tag found, continue looking

                if not booking_found:
                    print("❌ No available booking links. Refreshing...")
                    time.sleep(REFRESH_INTERVAL)
                    continue

                accept_cookies()

                # ✅ Enter Username
                try:
                    input_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']")))
                    input_field.clear()
                    input_field.send_keys(username)
                    print(f"✅ Entered username: {username}")
                except TimeoutException:
                    print("⚠ Username input field not found.")
                    continue

                try:
                    proceed_button = wait.until(EC.element_to_be_clickable((
                        By.XPATH, "//input[@type='submit' and contains(@value, 'Proceed')] | //button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'proceed')] | //a[contains(text(), 'Proceed')]"
                    )))
                    driver.execute_script("arguments[0].click();", proceed_button)
                    print("✅ Clicked 'Proceed with Booking' button")
                    time.sleep(1)
                except TimeoutException:
                    print("⚠ 'Proceed with Booking' button not found.")
                    continue

                accept_cookies()

                try:
                    confirm_button = wait.until(EC.element_to_be_clickable((
                        By.XPATH, "//input[@type='submit' and contains(@value, 'Confirm')] | //button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'confirm')] | //a[contains(text(), 'Confirm')]"
                    )))
                    driver.execute_script("arguments[0].click();", confirm_button)
                    print("🎉 Booking confirmed!")
                    warning_label.config(text="🎉 Booking Confirmed!", fg="lightgreen")
                    bot_running = False
                    return
                except TimeoutException:
                    print("⚠ 'Confirm Booking' button not found.")
                    continue

                print("❌ No available slots. Refreshing...")
                time.sleep(REFRESH_INTERVAL)

        except Exception as e:
            print(f"⚠ Error: {e}")
        finally:
            if driver:
                driver.quit()

    thread = threading.Thread(target=run_bot)
    thread.daemon = True
    thread.start()


def stop_booking():
    """Stops the booking bot and clears the terminal."""
    global bot_running, driver
    bot_running = False  # Stop the bot
    warning_label.config(text="⚠ Booking bot stopped!", fg="red")

    console_output.delete("1.0", tk.END)  # Clear terminal

    if driver:
        driver.quit()


def create_ui():
    """Creates a fullscreen Tkinter UI with a modern design."""
    root = tk.Tk()
    root.title("UCD Gym Booking Bot")
    root.configure(bg=BACKGROUND_COLOR)
    root.attributes("-fullscreen", True)

    tk.Label(root, text="UCD Gym Booking Bot", font=("Arial", 28, "bold"), fg=TEXT_COLOR, bg=BACKGROUND_COLOR).pack(pady=20)

    global warning_label
    warning_label = tk.Label(root, text="⚠ Run this 2 hours before your desired slot!", font=("Arial", 16, "bold"), fg=WARNING_COLOR, bg=BACKGROUND_COLOR)
    warning_label.pack(pady=5)

    tk.Label(root, text="Enter your UCD Username:", font=FONT, fg=TEXT_COLOR, bg=BACKGROUND_COLOR).pack(pady=5)
    username_entry = tk.Entry(root, font=FONT, width=25)
    username_entry.pack(pady=10)

    global console_output
    console_output = scrolledtext.ScrolledText(root, width=80, height=20, font=("Courier", 12), bg="#2A2A3C", fg="white")
    console_output.pack(pady=10)
    sys.stdout = TerminalOutput(console_output)

    start_button = tk.Button(root, text="Start Booking", command=lambda: start_booking(username_entry.get()), bg=BUTTON_COLOR, fg="white", font=("Arial", 16, "bold"))
    start_button.pack(pady=10)

    stop_button = tk.Button(root, text="Stop & Clear", command=stop_booking, bg=STOP_BUTTON_COLOR, fg="white", font=("Arial", 16, "bold"))
    stop_button.pack(pady=10)

    root.mainloop()


create_ui()
