# Mock conversion logic

conversion_rates = {
    "IN": {"currency": "INR", "rate": 80},
    "US": {"currency": "USD", "rate": 1},
    "EU": {"currency": "EUR", "rate": 0.9},
    "JP": {"currency": "JPY", "rate": 110},
}


def get_price_by_country(country_code):
    base_price_usd = 100  # USD
    country_code = country_code.upper()

    if country_code in conversion_rates:
        data = conversion_rates[country_code]
        return {
            "currency": data["currency"],
            "price": base_price_usd * data["rate"]
        }

    return {"currency": "USD", "price": base_price_usd}
