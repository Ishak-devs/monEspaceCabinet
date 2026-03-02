def close_discussion(driver):
    close_chat_script = """
    function findCloseButton() {
        let btn = document.querySelector('button[data-test-icon="close-small"]');
        if (btn) return btn;

        let svg = document.querySelector('svg[data-test-icon="close-small"]');
        if (svg && svg.closest('button')) return svg.closest('button');

        return Array.from(document.querySelectorAll('button')).find(b =>
            b.innerText.includes('Fermer votre conversation') ||
            (b.getAttribute('aria-label') && b.getAttribute('aria-label').includes('Fermer'))
        );
    }
    try {
        let target = findCloseButton();
        if (target) { target.click(); return "OK"; }
        return "Bouton non trouvé";
    } catch (e) {
        return "Erreur JS : " + e.message;
    }
    """
    return driver.execute_script(close_chat_script)
