"""Run this once to generate sample sales data: python data/generate_data.py"""
import pandas as pd
import random
from datetime import date, timedelta

random.seed(42)

categories = {
    "Electronics": ["Laptop", "Phone", "Tablet", "Headphones", "Smartwatch"],
    "Clothing":    ["Jacket", "Sneakers", "T-Shirt", "Jeans", "Hat"],
    "Food":        ["Coffee Beans", "Protein Bar", "Green Tea", "Olive Oil", "Honey"],
    "Books":       ["Python Crash Course", "Clean Code", "Atomic Habits", "Deep Work", "The Pragmatic Programmer"],
}

price_range = {
    "Electronics": (50, 1500),
    "Clothing":    (10, 200),
    "Food":        (5, 40),
    "Books":       (10, 50),
}

rows = []
start = date(2024, 1, 1)

for i in range(500):
    day = start + timedelta(days=random.randint(0, 364))
    category = random.choice(list(categories.keys()))
    product = random.choice(categories[category])
    lo, hi = price_range[category]
    revenue = round(random.uniform(lo, hi), 2)
    quantity = random.randint(1, 10)
    rows.append({
        "date": day,
        "category": category,
        "product": product,
        "quantity": quantity,
        "revenue": round(revenue * quantity, 2),
    })

df = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
import os
output = os.path.join(os.path.dirname(__file__), "sales.csv")
df.to_csv(output, index=False)
print(f"Generated {len(df)} rows -> {output}")
