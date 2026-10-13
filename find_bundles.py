"""Reproduce the bundle recommendations for one market and write reports/bundles_<country>.md.

Same cleaning and FP-Growth settings as the app's defaults. Usage: python find_bundles.py [Country]
"""
import sys
from pathlib import Path

import pandas as pd
from mlxtend.frequent_patterns import association_rules, fpgrowth
from mlxtend.preprocessing import TransactionEncoder

MIN_SUPPORT, MIN_CONFIDENCE, MIN_LIFT = 0.05, 0.30, 1.2   # app defaults
NON_PRODUCTS = {"POSTAGE", "Manual", "CARRIAGE", "DOTCOM POSTAGE"}


def main(country: str = "France") -> None:
    df = pd.read_csv("data/OnlineRetail.csv", encoding="ISO-8859-1", dtype={"InvoiceNo": str, "Description": str})
    df = df.dropna(subset=["InvoiceNo", "Description"])
    df["Description"] = df["Description"].str.strip()
    df = df[~df["InvoiceNo"].str.startswith("C") & (df["Quantity"] > 0)]
    sub = df[(df["Country"] == country) & ~df["Description"].isin(NON_PRODUCTS)]
    baskets = sub.groupby("InvoiceNo")["Description"].apply(lambda s: sorted(set(s))).tolist()

    te = TransactionEncoder()
    onehot = pd.DataFrame(te.fit(baskets).transform(baskets), columns=te.columns_)
    items = fpgrowth(onehot, min_support=MIN_SUPPORT, use_colnames=True)
    rules = association_rules(items, metric="lift", min_threshold=MIN_LIFT)
    rules = rules[rules["confidence"] >= MIN_CONFIDENCE]
    rules = rules[(rules["antecedents"].apply(len) == 1) & (rules["consequents"].apply(len) == 1)]
    rules["anchor"] = rules["antecedents"].apply(lambda s: next(iter(s)))
    rules["add_on"] = rules["consequents"].apply(lambda s: next(iter(s)))
    top = rules.sort_values(["lift", "confidence"], ascending=False).head(10)

    out = Path("reports"); out.mkdir(exist_ok=True)
    md = [f"# Bundle candidates: {country}", "",
          f"{len(baskets):,} invoices (cancellations, returns and postage lines removed). "
          f"FP-Growth with support >= {MIN_SUPPORT:.0%}, confidence >= {MIN_CONFIDENCE:.0%}, lift >= {MIN_LIFT}.", "",
          "| Anchor product | Add-on | Baskets with both | Confidence | Lift |", "|---|---|---|---|---|"]
    md += [f"| {r.anchor} | {r.add_on} | {r.support:.1%} | {r.confidence:.0%} | {r.lift:.1f}x |" for r in top.itertuples()]
    (out / f"bundles_{country.lower().replace(' ', '_')}.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "France")
