# from selenium.webdriver.common.by import By
#
#
# def find_buttons_conx(driver):
#     boutons_conx = driver.find_elements(
#         By.XPATH,
#         "//a[contains(@aria-label, 'Inviter') and contains(@aria-label, 'rejoindre votre réseau')]",
#     )
#     return boutons_conx
from telnetlib import EC

from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait

# def find_buttons_conx(driver):
#     boutons_conx = driver.find_elements(
#         By.XPATH,
#         "//*[.//*[@id='connect-small']]"
#     )
#     return boutons_conx


def find_buttons_conx(driver):
    boutons_conx = driver.find_elements(
        By.XPATH,
        "//button[.//svg[@id='connect-small']]"
    )
    return boutons_conx