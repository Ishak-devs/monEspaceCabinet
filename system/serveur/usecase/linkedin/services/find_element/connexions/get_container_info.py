from selenium.webdriver.common.by import By


def get_container_info(bouton):
    container = bouton.find_element(
        By.XPATH, "./ancestor::div[@role='listitem'][1]"
    )
    print(f"Container text: {container.text}")

    infos_profiles = container.text.lower().replace("\n", "").strip()
    return infos_profiles, container