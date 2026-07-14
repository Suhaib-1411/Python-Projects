import time
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import CHROME_PROFILE_DIR
from database import log_message

class WhatsAppAutomation:
    def __init__(self):
        options = Options()
        # Saves your WhatsApp login session so you don't scan every time
        options.add_argument(f"--user-data-dir={CHROME_PROFILE_DIR}")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        # Modern Selenium automatically manages Chrome drivers natively! 
        # No extra driver managers or services needed.
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 30)

    def open_whatsapp(self):
        print("\n[*] Opening WhatsApp Web. Please scan the QR code if prompted...")
        self.driver.get("https://web.whatsapp.com")
        # Wait until the main chat list interface loads
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="chat-list-search"]')))
        print("[+] WhatsApp Web successfully loaded!")

    def send_message(self, phone, message):
        try:
            phone = phone.replace("+", "").replace(" ", "").strip()
            encoded_msg = urllib.parse.quote(message)
            url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_msg}"
            
            self.driver.get(url)
            
            # Wait for the send button to appear and become clickable
            send_btn = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//span[@data-testid="send"]|//button[@data-testid="compose-btn-send"]')
            ))
            time.sleep(2) 
            send_btn.click()
            time.sleep(3) 
            
            log_message(phone, message, "Sent")
            print(f"[✔] Message successfully sent to {phone}")
            return True
        except Exception as e:
            log_message(phone, message, "Failed")
            print(f"[✘] Failed to send message to {phone}. Error: {str(e)}")
            return False

    def close(self):
        self.driver.quit()