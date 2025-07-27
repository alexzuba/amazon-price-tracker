import requests
from bs4 import BeautifulSoup
import json
import time

CONFIG_FILE = "config.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "it-IT,it;q=0.9"
}

def load_config(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Errore nel caricamento del file di configurazione: {e}")
        return None

def get_price(product_url):
    try:
        response = requests.get(product_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")

        # Prova più selettori per maggiore compatibilità
        price_tag = (
            soup.select_one("#priceblock_ourprice") or
            soup.select_one("#priceblock_dealprice") or
            soup.select_one("#corePriceDisplay_desktop_feature_div span.a-offscreen")
        )

        if price_tag:
            price_text = price_tag.text.strip().replace("€", "").replace(",", ".")
            return float(price_text)
        else:
            print("❌ Prezzo non trovato nella pagina.")
            return None

    except Exception as e:
        print(f"⚠️ Errore durante il recupero del prezzo: {e}")
        return None

def main():
    config = load_config(CONFIG_FILE)
    if not config:
        return

    product_url = config.get("product_url")
    target_price = config.get("target_price")

    if not product_url or not target_price:
        print("❌ Configurazione non valida. Verifica il file config.json.")
        return

    print("🔍 Controllo prezzo per:")
    print(product_url)

    current_price = get_price(product_url)

    if current_price is None:
        print("❌ Prezzo non disponibile.")
    else:
        print(f"💰 Prezzo attuale: {current_price:.2f} €")
        print(f"🎯 Prezzo target:  {target_price:.2f} €")

        if current_price <= target_price:
            print("✅ Prezzo sotto soglia! Puoi acquistare! 🎉")
            # Qui collegheremo la notifica
        else:
            print("📉 Prezzo ancora troppo alto.")

if __name__ == "__main__":
    main()
