import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify
import os


app = Flask(__name__)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render's assigned port or default to 5000
    app.run(host="0.0.0.0", port=port)

@app.route("/fuel", methods=["GET"])
def get_fuel_prices():
    URL = "https://ceypetco.gov.lk/marketing-sales/"
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.find_all("div", class_="card")

    prices = {}

    for card in cards:
        texts = card.get_text(separator="\n", strip=True).split("\n")
        fuel_name = None
        price = None

        for i, text in enumerate(texts):
            if "Price (Rs. per Ltr):" in text:
                price = text.replace("Price (Rs. per Ltr):", "").strip()
                if i > 0:
                    fuel_name = texts[i - 1].strip()
                break

        if fuel_name and price:
            prices[fuel_name] = price

    return jsonify(prices)

if __name__ == "__main__":
    app.run()
