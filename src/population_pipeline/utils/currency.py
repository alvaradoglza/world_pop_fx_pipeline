import pycountry
from babel.numbers import get_territory_currencies

def iso3_to_currency(code: str) -> str | None:

    if not code:
        return None

    code = code.upper().strip()

    if len(code) == 2:
        country = pycountry.countries.get(alpha_2=code)
    else:                         
        country = pycountry.countries.get(alpha_3=code)

    if not country:
        return None

    curr_list = get_territory_currencies(country.alpha_2, tender=True)
    if curr_list:
        return curr_list[0]

    cur = pycountry.currencies.get(numeric=country.numeric)
    return cur.alpha_3 if cur else None
