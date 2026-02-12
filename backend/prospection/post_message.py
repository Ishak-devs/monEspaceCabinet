import random
import time

from data.prompt.post_prompt import post_prompt
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from data.call_groq import call_groq


def post_message(driver, post):

    try:
        wait = WebDriverWait(driver, 10)
        post_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//p[contains(text(), 'Commencer un post')]")
            )
        )
        post_input.click()
        time.sleep(random.uniform(3, 5))
        print("Message ouvert")

        editor = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div[role='textbox'], ql-editor")
            )
        )

        instruction = "Aide nous à généré un message pour Linkedin"
        prompt = post_prompt(instruction)
        message_ia = call_groq(prompt)
        print(f"Message généré : {message_ia}")

        if message_ia:
            editor.click()
            for char in message_ia:
                editor.send_keys(char)
                time.sleep(0.05)
                print(f"Char sent: {char}")

    except Exception as e:
        print(f"Erreur lors de l'ouverture du message : {e}")
