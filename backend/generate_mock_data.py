from pathlib import Path

import numpy as np
import pandas as pd


def generate_sales_data() -> pd.DataFrame:
    rng = np.random.default_rng(42)
    row_count = 10_000
    dates = pd.date_range("2024-01-01", "2026-12-31", freq="D")
    categories = rng.choice(
        ["Technology", "Furniture", "Office Supplies"],
        size=row_count,
        p=[0.3, 0.25, 0.45],
    )
    price_multiplier = np.where(
        categories == "Technology", 2.0, np.where(categories == "Furniture", 1.5, 0.5)
    )
    revenue = np.round(
        rng.lognormal(mean=5.5, sigma=0.8, size=row_count) * price_multiplier, 2
    )
    profit_margin = rng.uniform(-0.1, 0.35, size=row_count)

    return pd.DataFrame(
        {
            "order_id": [f"ORD-{i:06d}" for i in range(1, row_count + 1)],
            "order_date": rng.choice(dates, size=row_count),
            "region": rng.choice(["North", "South", "East", "West"], size=row_count),
            "category": categories,
            "revenue": revenue,
            "profit": np.round(revenue * profit_margin, 2),
        }
    )


def main() -> None:
    data = generate_sales_data()
    output_path = Path(__file__).resolve().parent / "sales_data.parquet"
    data.to_parquet(output_path, engine="pyarrow", index=False)
    print(f"Generated {len(data):,} rows at {output_path}")


if __name__ == "__main__":
    main()
