import random
import time
import traceback
from datetime import datetime, timezone

from data.prompt.post_prompt import post_prompt
from database import supabase_client
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from typing_extensions import Any

from data.call_groq import call_groq


def post_message(driver, post, config_db):

    yield "On va checker la derniere fois qu'on a posté..."
    print("On va checker la derniere fois qu'on a posté...")

    res = (
        supabase_client.table("posts")
        .select("id, last_posted_at")
        .eq("user_id", config_db.get("user_id"))
        # .neq("id", config_db.get("id"))
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )

    print(f"resultat de la requete sur la table posts: {res}")

    data: Any = res.data

    if list(res.data) and len(res.data) > 0:
        row: dict = data[0]

        print(f"data : {data}")
        now = datetime.now(timezone.utc)

        last_post = datetime.fromisoformat(
            row["last_posted_at"].replace("+00", "+00:00")
        )
        print(f"last_post: {last_post}")

        row_id = row["id"]
        print(f"row_id: {row_id}")

        # delta = now - last_post
        delta = now.replace(tzinfo=None) - last_post.replace(tzinfo=None)
        post_recent = delta.days < 2

        print(
            f"DEBUG: last_post = {last_post}, now = {now}, delta = {delta}, post_recent = {post_recent}"
        )
        # yield "On va checker la derniere fois qu'on a posté..."
        time.sleep(1)

        if post_recent:
            yield "On à poster récemment... On saute cette étape aujourd'hui"
            print("On a poster récemment...on skip")

        else:
            full_name = config_db.get("full_name")
            telephone = config_db.get("telephone")
            cabinet_name = config_db.get("cabinet_name")
            print(
                "Infos pour post message:"
                f"Full Name: {full_name}, Telephone: {telephone}, Cabinet Name: {cabinet_name}"
            )

            try:
                # instruction = "Donne un message court en une phrase"
                prompt = post_prompt(post, full_name, telephone, cabinet_name)
                print(f"POST : {post}")

                message_ia = call_groq(prompt)
                print(f"Message généré : {message_ia}")

                # wait = WebDriverWait(driver, 30)
                time.sleep(random.uniform(5, 10))
                post_input = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//p[contains(text(), 'Commencer un post')]")
                    )
                )
                post_input.click()
                time.sleep(random.uniform(3, 5))
                print("Message ouvert")

                js_find_editor = """
                        function findDeep(sel, root = document) {
                            let n = root.querySelector(sel);
                            if (n) return n;
                            let all = root.querySelectorAll('*');
                            for (let e of all) {
                                if (e.shadowRoot) {
                                    let res = findDeep(sel, e.shadowRoot);
                                    if (res) return res;
                                }
                            }
                            return null;
                        }
                        return findDeep("div[contenteditable='true'], div[role='textbox'], .ql-editor");
                        """

                editor = driver.execute_script(js_find_editor)
                print("Editor found")

                if message_ia:
                    driver.execute_script("arguments[0].focus();", editor)
                    time.sleep(random.uniform(5, 10))
                    editor.click()
                    actions = ActionChains(driver)
                    actions.move_to_element(editor)
                    actions.click()
                    actions.perform()

                    print("Editor clicked")
                    yield "Nous avons pas posté depuis un moment..."
                    yield "Nous allons saisir un post..."
                    time.sleep(random.uniform(5, 10))
                    yield "✍️ Écriture du message en cours..."

                    print("[DEBUG-STEP] Lancement post message")
                    for char in message_ia:
                        # time.sleep(3)
                        actions.send_keys(char)
                        actions.perform()
                        time.sleep(random.uniform(0.25, 0.35))
                    time.sleep(random.uniform(5, 10))

                    try:
                        time.sleep(random.uniform(5, 10))
                        from script_element_xpath.post_button import post_button

                        driver.execute_script(post_button())
                        # if resultat == "BOUTON_CLIQUE":
                        print("✅ Message publié !")
                        yield "✅ Post publié..."
                        time.sleep(random.uniform(5, 10))

                        try:
                            print(
                                "tentative de mise à jour de la date de dernière publication"
                            )

                            supabase_client.table("posts").update(
                                {"last_posted_at": datetime.now().isoformat()}
                            ).eq("id", row_id).execute()

                            print("✅ Date de dernière publication mise à jour")

                        except Exception as e:
                            print(
                                f"❌ Erreur lors de la mise à jour de la date de dernière publication : {e}"
                            )

                    except Exception:
                        print("❌ Bouton introuvable par le script JS")
                        traceback.print_exc()
                        print("------------------------")

            except Exception as e:
                print(f"Erreur : {e}")
