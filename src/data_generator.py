from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


CATEGORIES = {
    "Ethnic Wear": ["Kurta Set", "Anarkali Dress", "Saree", "Palazzo Set"],
    "Western Wear": ["Bodycon Dress", "Denim Jacket", "Crop Top", "Wide-leg Jeans"],
    "Footwear": ["Sneakers", "Heels", "Juttis", "Sandals"],
    "Activewear": ["Training Tee", "Leggings", "Sports Bra", "Track Pants"],
    "Accessories": ["Handbag", "Sunglasses", "Belt", "Scarf"],
    "Beauty": ["Lip Tint", "Kajal", "Serum", "Compact"],
}

SIZES = ["XS", "S", "M", "L", "XL", "XXL", "One Size"]
CHANNELS = ["App", "Web", "Influencer", "Marketplace", "Retail Partner"]
TIERS = ["Tier 1", "Tier 2", "Tier 3"]
RETURN_REASONS = [
    "Size too small",
    "Size too large",
    "Fabric expectation mismatch",
    "Color mismatch",
    "Damaged item",
    "Late delivery",
    "Changed mind",
    "Not returned",
]

CITY_POOL = {
    "Tier 1": [
        ("Bengaluru", "Karnataka"),
        ("Delhi NCR", "Delhi"),
        ("Mumbai", "Maharashtra"),
        ("Hyderabad", "Telangana"),
        ("Chennai", "Tamil Nadu"),
        ("Pune", "Maharashtra"),
    ],
    "Tier 2": [
        ("Jaipur", "Rajasthan"),
        ("Lucknow", "Uttar Pradesh"),
        ("Indore", "Madhya Pradesh"),
        ("Kochi", "Kerala"),
        ("Surat", "Gujarat"),
        ("Chandigarh", "Punjab"),
    ],
    "Tier 3": [
        ("Jodhpur", "Rajasthan"),
        ("Mysuru", "Karnataka"),
        ("Guntur", "Andhra Pradesh"),
        ("Udaipur", "Rajasthan"),
        ("Siliguri", "West Bengal"),
        ("Ajmer", "Rajasthan"),
    ],
}


def _category_profile(category: str) -> dict[str, float]:
    profiles = {
        "Ethnic Wear": {"price": 1990, "margin": 0.48, "return": 0.24},
        "Western Wear": {"price": 1590, "margin": 0.44, "return": 0.31},
        "Footwear": {"price": 2290, "margin": 0.42, "return": 0.28},
        "Activewear": {"price": 1290, "margin": 0.39, "return": 0.22},
        "Accessories": {"price": 990, "margin": 0.56, "return": 0.12},
        "Beauty": {"price": 690, "margin": 0.52, "return": 0.07},
    }
    return profiles[category]


def generate_orders(rows: int = 9000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    start = pd.Timestamp("2025-01-01")
    dates = start + pd.to_timedelta(rng.integers(0, 455, rows), unit="D")
    categories = rng.choice(list(CATEGORIES), rows, p=[0.22, 0.25, 0.16, 0.13, 0.14, 0.10])

    records = []
    for idx, category in enumerate(categories):
        profile = _category_profile(category)
        product_name = rng.choice(CATEGORIES[category])
        size = "One Size" if category in {"Accessories", "Beauty"} else rng.choice(SIZES[:-1], p=[0.09, 0.19, 0.27, 0.22, 0.15, 0.08])
        tier = rng.choice(TIERS, p=[0.46, 0.34, 0.20])
        city, state = CITY_POOL[tier][rng.integers(0, len(CITY_POOL[tier]))]
        channel = rng.choice(CHANNELS, p=[0.48, 0.25, 0.11, 0.10, 0.06])

        base_price = max(299, rng.normal(profile["price"], profile["price"] * 0.24))
        units = int(rng.choice([1, 1, 1, 2, 2, 3], p=[0.50, 0.18, 0.12, 0.11, 0.06, 0.03]))
        discount_rate = float(np.clip(rng.normal(0.18, 0.09), 0.02, 0.48))
        gross_revenue = round(base_price * units, 2)
        discount = round(gross_revenue * discount_rate, 2)
        net_sales = gross_revenue - discount

        size_risk = 0.0
        if size in {"XS", "XXL"}:
            size_risk += 0.11
        if category in {"Western Wear", "Footwear"} and size in {"S", "XL", "XXL"}:
            size_risk += 0.07
        tier_risk = {"Tier 1": 0.03, "Tier 2": 0.01, "Tier 3": -0.02}[tier]
        channel_risk = {"Influencer": 0.06, "Marketplace": 0.04, "App": 0.01, "Web": 0.0, "Retail Partner": -0.03}[channel]
        return_probability = float(np.clip(profile["return"] + size_risk + tier_risk + channel_risk + rng.normal(0, 0.035), 0.02, 0.68))
        returned = rng.random() < return_probability

        product_cost = round(net_sales * (1 - profile["margin"]) * rng.normal(1.0, 0.05), 2)
        shipping_cost = round(55 + units * rng.normal(37, 8) + (tier == "Tier 3") * 28, 2)
        payment_fee = round(net_sales * rng.uniform(0.014, 0.024), 2)
        return_logistics_cost = round((shipping_cost * rng.uniform(0.85, 1.35) + 35) if returned else 0, 2)
        refund_amount = round(net_sales * rng.uniform(0.86, 1.0), 2) if returned else 0
        return_adjusted_profit = round(net_sales - product_cost - shipping_cost - payment_fee - return_logistics_cost - refund_amount, 2)

        if not returned:
            reason = "Not returned"
        elif size in {"XS", "S"} and rng.random() < 0.42:
            reason = "Size too small"
        elif size in {"XL", "XXL"} and rng.random() < 0.39:
            reason = "Size too large"
        else:
            reason = rng.choice(RETURN_REASONS[:-1], p=[0.18, 0.14, 0.25, 0.13, 0.10, 0.09, 0.11])

        sku = f"{category[:2].upper().replace(' ', '')}-{product_name[:3].upper().replace(' ', '')}-{size.replace(' ', '')}"
        customer_id = f"C{rng.integers(10000, 99999)}"
        cohort_month = str(pd.Timestamp(dates[idx]).to_period("M"))

        records.append(
            {
                "order_id": f"ORD{idx + 100000}",
                "order_date": dates[idx].date().isoformat(),
                "customer_id": customer_id,
                "cohort_month": cohort_month,
                "category": category,
                "product_name": product_name,
                "sku": sku,
                "size": size,
                "units": units,
                "gross_revenue": gross_revenue,
                "discount": discount,
                "net_sales": round(net_sales, 2),
                "product_cost": product_cost,
                "shipping_cost": shipping_cost,
                "payment_fee": payment_fee,
                "returned": bool(returned),
                "return_reason": reason,
                "return_logistics_cost": return_logistics_cost,
                "refund_amount": refund_amount,
                "return_adjusted_profit": return_adjusted_profit,
                "city": city,
                "state": state,
                "city_tier": tier,
                "channel": channel,
                "inventory_on_hand": int(max(0, rng.normal(180, 80))),
                "stockout_risk": round(float(np.clip(rng.beta(2.0, 4.0) + (category == "Western Wear") * 0.13, 0, 1)), 3),
                "markdown_risk": round(float(np.clip(rng.beta(2.2, 5.0) + returned * 0.17, 0, 1)), 3),
            }
        )

    df = pd.DataFrame(records)
    return df.sort_values("order_date").reset_index(drop=True)


def ensure_sample_data(path: str | Path = "data/fashion_orders_sample.csv") -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        generate_orders().to_csv(target, index=False)
    return target


if __name__ == "__main__":
    output = ensure_sample_data()
    print(f"Wrote {output}")
