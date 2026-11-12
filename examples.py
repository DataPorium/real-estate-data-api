"""US real estate data API: homes for sale, rentals, sold homes, price cuts and housing markets by ZIP code

Runnable examples: each one is a single request to the DataPorium API.

    python examples.py                      # list the examples
    python examples.py homes-for-sale
    python examples.py homes-for-sale --csv out.csv
    python examples.py homes-for-sale --json       # the raw answer

Needs a DataPorium API key in the DATAPORIUM_API_KEY environment variable.
"""
from __future__ import annotations

import argparse
import json
import sys

from dataporium import DataPorium, to_frame

# name: (question, method, parameters, key of the rows inside the answer)
EXAMPLES = {
    'homes-for-sale': ('Homes for sale in a ZIP code, 3+ bedrooms under $900,000', 'properties', {'zip': '92602', 'beds_min': 3, 'price_max': 900000, 'sort': 'newest', 'limit': 25}, 'homes'),
    'homes-for-rent': ('Homes for rent in a city', 'properties', {'city': 'Austin', 'state': 'TX', 'status': 'rent', 'beds_min': 2, 'price_max': 3000, 'limit': 25}, 'homes'),
    'homes-sold': ('Homes sold in the last 90 days', 'properties', {'zip': '78704', 'status': 'sold', 'sold_within_days': 90, 'sort': 'newest', 'limit': 25}, 'homes'),
    'home-by-address': ('One home in full, by address', 'properties', {'address': '41 Carpenteria, Irvine CA'}, None),
    'price-cuts': ('Homes with a price cut in the last 7 days, biggest cut first', 'properties', {'city': 'Irvine', 'state': 'CA', 'price_cut': True, 'price_cut_within_days': 7, 'sort': 'biggest_cut', 'limit': 25}, 'homes'),
    'price-changes': ('Every price cut, increase and relist in a ZIP code', 'realestate_price_changes', {'zip_code': '92602', 'include_events': True}, None),
    'below-area-price': ("Homes priced at least 10% below the ZIP code's price per square foot", 'properties', {'zip': '85032', 'below_area_ppsf_pct': 10, 'sort': 'best_value', 'limit': 25}, 'homes'),
    'stale-listings': ('Homes on the market for more than 90 days in the whole selling effort', 'properties', {'county': 'Maricopa', 'state': 'AZ', 'true_dom_min': 90, 'sort': 'dom_desc', 'limit': 25}, 'homes'),
    'monthly-payment': ('Homes with an estimated monthly payment (10% down, 6.5% rate)', 'properties', {'zip': '75034', 'with_payment': True, 'down_payment_pct': 10, 'interest_rate': 6.5, 'limit': 25}, 'homes'),
    'property-tax': ('Property tax rates of a ZIP code', 'property_tax', {'zip': '77493'}, None),
    'mortgage-lending': ('Home purchase loans in a county: applications, approval rate, loan sizes, top lenders', 'mortgage_lending_summary', {'state': 'TX', 'county': 'Travis', 'purpose': 'purchase', 'top': 10}, None),
    'local-jobs': ('Unemployment in a county, month by month', 'local_jobs', {'area_type': 'county', 'state': 'TX', 'county': 'Travis', 'date_from': '2024-01'}, None),
    'where-people-move': ('Counties of a state ranked by people moving in, net', 'migration', {'area_type': 'county', 'state': 'FL', 'latest': True, 'sort': 'net_people', 'order': 'desc', 'limit': 25}, None),
    'new-home-permits': ('Metro areas ranked by new homes permitted', 'building_permits', {'area_type': 'metro', 'latest': True, 'sort': 'units_total', 'order': 'desc', 'limit': 25}, None),
    'mortgage-denial-rates': ('Counties of a state ranked by mortgage denial rate', 'mortgage_lending_areas', {'area_type': 'county', 'state': 'CA', 'sort': 'denial_rate', 'order': 'desc', 'min_applications': 500, 'limit': 25}, None),
    'lowest-unemployment': ('Counties of a state ranked by unemployment, newest month', 'local_jobs', {'area_type': 'county', 'state': 'NC', 'latest': True, 'sort': 'unemployment_rate', 'order': 'asc', 'limit': 25}, None),
}


def rows(answer, key=None):
    """The answer as a DataFrame, or None when it has no table in it."""
    try:
        frame = to_frame(answer, key=key)
    except (KeyError, TypeError):
        return None
    return frame if len(frame) > 1 else None  # one record reads better as JSON


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("example", nargs="?", help="Name of the example; leave out to list them")
    parser.add_argument("--csv", help="Save the rows to this CSV file")
    parser.add_argument("--json", action="store_true", help="Print the raw JSON answer")
    parser.add_argument("--rows", type=int, default=20, help="Rows to print (default 20)")
    args = parser.parse_args(argv)

    if not args.example:
        width = max(len(name) for name in EXAMPLES)
        for name, (question, *_rest) in EXAMPLES.items():
            print(f"{name:<{width}}  {question}")
        return 0
    if args.example not in EXAMPLES:
        parser.error(f"unknown example {args.example!r}; run without arguments to list them")

    question, method, params, key = EXAMPLES[args.example]
    print(f"{question}\n  dp.{method}({', '.join(f'{k}={v!r}' for k, v in params.items())})\n")
    answer = DataPorium().call(method, **params)

    frame = None if args.json else rows(answer, key)
    if frame is None:
        print(json.dumps(answer, indent=2, default=str)[:20000])
    else:
        print(frame.head(args.rows).to_string(max_colwidth=40))
        print(f"\n{len(frame)} rows")
    if args.csv:
        if frame is None:
            frame = rows(answer, key)
        if frame is None:
            print("This answer has no table to save.", file=sys.stderr)
            return 1
        frame.to_csv(args.csv, index=False)
        print(f"Saved {args.csv}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
