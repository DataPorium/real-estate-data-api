# US real estate data API: homes for sale, rentals, sold homes, price cuts and housing markets by ZIP code

Search US homes for sale, for rent, pending and sold in the last 12 months, by ZIP code, city, county or state. Get price cuts and relists with the real listed date, look up one home by address, estimate the monthly payment, and read the market around it: property tax, mortgage lending, jobs, new home permits and people moving in and out. Every example is one request to the [DataPorium](https://dataporium.tech) REST API, shown in Python and curl.

## Quick start

```bash
pip install git+https://github.com/DataPorium/dataporium-python.git
export DATAPORIUM_API_KEY="YOUR_API_KEY"
```

```python
from dataporium import DataPorium, to_frame

dp = DataPorium()   # reads DATAPORIUM_API_KEY
answer = dp.properties(zip="92602", beds_min=3, price_max=900000, sort="newest", limit=25)
print(to_frame(answer, key="homes").head())
```

Or run any example below from this repository:

```bash
git clone https://github.com/DataPorium/real-estate-data-api.git
cd real-estate-data-api
pip install -r requirements.txt
python examples.py           # list the examples
python examples.py homes-for-sale     # run one
python examples.py homes-for-sale --csv out.csv
```

## What you can get

| Question | Example | Endpoint |
|---|---|---|
| Homes for sale in a ZIP code, 3+ bedrooms under $900,000 | [`homes-for-sale`](#homes-for-sale) | `GET /properties` |
| Homes for rent in a city | [`homes-for-rent`](#homes-for-rent) | `GET /properties` |
| Homes sold in the last 90 days | [`homes-sold`](#homes-sold) | `GET /properties` |
| One home in full, by address | [`home-by-address`](#home-by-address) | `GET /properties` |
| Homes with a price cut in the last 7 days, biggest cut first | [`price-cuts`](#price-cuts) | `GET /properties` |
| Every price cut, increase and relist in a ZIP code | [`price-changes`](#price-changes) | `GET /realestate-price-changes` |
| Homes priced at least 10% below the ZIP code's price per square foot | [`below-area-price`](#below-area-price) | `GET /properties` |
| Homes on the market for more than 90 days in the whole selling effort | [`stale-listings`](#stale-listings) | `GET /properties` |
| Homes with an estimated monthly payment (10% down, 6.5% rate) | [`monthly-payment`](#monthly-payment) | `GET /properties` |
| Property tax rates of a ZIP code | [`property-tax`](#property-tax) | `GET /property-tax` |
| Home purchase loans in a county: applications, approval rate, loan sizes, top lenders | [`mortgage-lending`](#mortgage-lending) | `GET /mortgage-lending/summary` |
| Unemployment in a county, month by month | [`local-jobs`](#local-jobs) | `GET /local-jobs` |
| Counties of a state ranked by people moving in, net | [`where-people-move`](#where-people-move) | `GET /migration` |
| Metro areas ranked by new homes permitted | [`new-home-permits`](#new-home-permits) | `GET /building-permits` |
| Counties of a state ranked by mortgage denial rate | [`mortgage-denial-rates`](#mortgage-denial-rates) | `GET /mortgage-lending/areas` |
| Counties of a state ranked by unemployment, newest month | [`lowest-unemployment`](#lowest-unemployment) | `GET /local-jobs` |

## Find homes

<a id="homes-for-sale"></a>
### Homes for sale in a ZIP code, 3+ bedrooms under $900,000

```python
dp.properties(zip="92602", beds_min=3, price_max=900000, sort="newest", limit=25)
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/properties?zip=92602&beds_min=3&price_max=900000&sort=newest&limit=25"
```

Search by `zip` (up to 25, comma-separated), `city` and `state`, `county` and `state`, or `state` alone. More filters: baths, square feet, lot, year built, style, HOA, days on market.

<a id="homes-for-rent"></a>
### Homes for rent in a city

```python
dp.properties(city="Austin", state="TX", status="rent", beds_min=2, price_max=3000, limit=25)
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/properties?city=Austin&state=TX&status=rent&beds_min=2&price_max=3000&limit=25"
```

For rentals, `price_min` and `price_max` are the monthly rent.

<a id="homes-sold"></a>
### Homes sold in the last 90 days

```python
dp.properties(zip="78704", status="sold", sold_within_days=90, sort="newest", limit=25)
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/properties?zip=78704&status=sold&sold_within_days=90&sort=newest&limit=25"
```

Sold homes cover the last 12 months, with the sold price against the last list price.

<a id="home-by-address"></a>
### One home in full, by address

```python
dp.properties(address="41 Carpenteria, Irvine CA")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/properties?address=41%20Carpenteria,%20Irvine%20CA"
```

Any common spelling of the address works. The answer has the listing history and a comparison with nearby homes; `radius_miles` and the `nearby_*` filters set the comparison.

## Price cuts and deals

<a id="price-cuts"></a>
### Homes with a price cut in the last 7 days, biggest cut first

```python
dp.properties(city="Irvine", state="CA", price_cut=True, price_cut_within_days=7, sort="biggest_cut", limit=25)
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/properties?city=Irvine&state=CA&price_cut=true&price_cut_within_days=7&sort=biggest_cut&limit=25"
```

`cut_min` and `cut_pct_min` keep only cuts of at least so many dollars or percent since the home was first listed.

<a id="price-changes"></a>
### Every price cut, increase and relist in a ZIP code

```python
dp.realestate_price_changes(zip_code="92602", include_events=True)
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/realestate-price-changes?zip_code=92602&include_events=true"
```

With true dates from each home's own listing history, so a relisted home does not look new.

<a id="below-area-price"></a>
### Homes priced at least 10% below the ZIP code's price per square foot

```python
dp.properties(zip="85032", below_area_ppsf_pct=10, sort="best_value", limit=25)
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/properties?zip=85032&below_area_ppsf_pct=10&sort=best_value&limit=25"
```

<a id="stale-listings"></a>
### Homes on the market for more than 90 days in the whole selling effort

```python
dp.properties(county="Maricopa", state="AZ", true_dom_min=90, sort="dom_desc", limit=25)
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/properties?county=Maricopa&state=AZ&true_dom_min=90&sort=dom_desc&limit=25"
```

True days on market count earlier listings of the same home too, so relisting does not reset the clock.

<a id="monthly-payment"></a>
### Homes with an estimated monthly payment (10% down, 6.5% rate)

```python
dp.properties(zip="75034", with_payment=True, down_payment_pct=10, interest_rate=6.5, limit=25)
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/properties?zip=75034&with_payment=true&down_payment_pct=10&interest_rate=6.5&limit=25"
```

Without the payment inputs, the payment uses 20% down and the latest average 30-year fixed rate.

## Housing market of an area

<a id="property-tax"></a>
### Property tax rates of a ZIP code

```python
dp.property_tax(zip="77493")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/property-tax?zip=77493"
```

Also by `city` or `county`, with `state`.

<a id="mortgage-lending"></a>
### Home purchase loans in a county: applications, approval rate, loan sizes, top lenders

```python
dp.mortgage_lending_summary(state="TX", county="Travis", purpose="purchase", top=10)
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/mortgage-lending/summary?state=TX&county=Travis&purpose=purchase&top=10"
```

Yearly since 2018. `loan_type` (conventional, fha, va, usda) and `occupancy` (primary, second_home, investment) narrow it.

<a id="local-jobs"></a>
### Unemployment in a county, month by month

```python
dp.local_jobs(area_type="county", state="TX", county="Travis", date_from="2024-01")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/local-jobs?area_type=county&state=TX&county=Travis&date_from=2024-01"
```

## Rank areas

<a id="where-people-move"></a>
### Counties of a state ranked by people moving in, net

```python
dp.migration(area_type="county", state="FL", latest=True, sort="net_people", order="desc", limit=25)
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/migration?area_type=county&state=FL&latest=true&sort=net_people&order=desc&limit=25"
```

From where households file their federal tax returns. `include_top=true` adds the 10 largest origins and destinations.

<a id="new-home-permits"></a>
### Metro areas ranked by new homes permitted

```python
dp.building_permits(area_type="metro", latest=True, sort="units_total", order="desc", limit=25)
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/building-permits?area_type=metro&latest=true&sort=units_total&order=desc&limit=25"
```

<a id="mortgage-denial-rates"></a>
### Counties of a state ranked by mortgage denial rate

```python
dp.mortgage_lending_areas(area_type="county", state="CA", sort="denial_rate", order="desc", min_applications=500, limit=25)
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/mortgage-lending/areas?area_type=county&state=CA&sort=denial_rate&order=desc&min_applications=500&limit=25"
```

<a id="lowest-unemployment"></a>
### Counties of a state ranked by unemployment, newest month

```python
dp.local_jobs(area_type="county", state="NC", latest=True, sort="unemployment_rate", order="asc", limit=25)
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/local-jobs?area_type=county&state=NC&latest=true&sort=unemployment_rate&order=asc&limit=25"
```

## Answers

Every answer is JSON. Many are a list of rows; paged answers hold their rows under `rows` with `total`, `limit` and `offset`. `to_frame(answer)` in the Python library finds the rows and returns a pandas DataFrame. Each endpoint and all of its parameters are described in the [API documentation](https://dataporium.tech/api-docs), and `print(dp.describe("<method>"))` shows them in Python.

## Use it in Claude, ChatGPT or Cursor

To rank ZIP codes, cities, counties and metros on dozens of housing measures at once (rent yield, price growth, inventory, crime and more), or to get the full picture of one area (market history, property tax, crime, demographics, climate risk, rents by bedroom count), connect the [DataPorium MCP server](https://github.com/DataPorium/dataporium-mcp) and ask in plain language. Its `search_housing_areas` and `get_housing_area_insights` tools do this in one call.

## Ready-made scripts

- [home-price-cut-finder](https://github.com/DataPorium/home-price-cut-finder): save the biggest price cuts of an area to CSV

## Get an API key

Sign up at [dataporium.tech](https://dataporium.tech/pricing) and subscribe to the Premium plan; the key is in your account settings. It works for the REST API (600 requests per minute) and the MCP server. Send it in the `apikey` header, as above; a `?apikey=` query parameter also works, but a key in a URL can end up in logs. Keep the key out of code you commit or share.

## More

- Python library: [dataporium-python](https://github.com/DataPorium/dataporium-python)
- JavaScript and TypeScript library: [dataporium-js](https://github.com/DataPorium/dataporium-js)
- Examples in curl, R, Google Sheets and Excel: [financial-data-api](https://github.com/DataPorium/financial-data-api)
- AI assistants: [dataporium-mcp](https://github.com/DataPorium/dataporium-mcp)
- API documentation: <https://dataporium.tech/api-docs>

## License

The code in this repository is released under the [MIT License](LICENSE). Use of the API and its data is governed by the DataPorium [Terms of Use](https://dataporium.tech/terms-of-use). Data is for information only and is not investment advice.
