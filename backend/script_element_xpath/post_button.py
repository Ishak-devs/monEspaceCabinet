def post_button():
    return """
    (function() {
        function findDeep(root, targetText) {
            // 1. On cherche dans les éléments enfants classiques
            const buttons = Array.from(root.querySelectorAll('button'));
            for (let btn of buttons) {
                const txt = (btn.innerText || btn.textContent || "").toLowerCase().trim();
                if (txt === targetText) return btn;
            }

            // 2. On cherche dans TOUS les éléments pour voir s'ils ont un Shadow Root
            const allElements = root.querySelectorAll('*');
            for (let el of allElements) {
                if (el.shadowRoot) {
                    const found = findDeep(el.shadowRoot, targetText);
                    if (found) return found;
                }
            }
            return null;
        }

        const btn = findDeep(document, 'publier');

        if (btn) {
            btn.removeAttribute('disabled');
            btn.disabled = false;
            btn.classList.remove('artdeco-button--disabled');
            btn.click();
            return "BOUTON_CLIQUE_DEEP";
        }

        // Si vraiment rien, on liste les 10 premiers boutons pour comprendre
        const sample = Array.from(document.querySelectorAll('button'))
                        .slice(0, 10)
                        .map(b => b.innerText.trim())
                        .join(' | ');
        return "RIEN_DU_TOUT - Exemples : " + sample;
    })();
    """
