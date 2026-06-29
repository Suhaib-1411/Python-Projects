"""Generate sample Excel file for Task 7 demo"""
import pandas as pd
import numpy as np

np.random.seed(42)
n = 50

departments = ["Engineering", "Marketing", "HR", "Finance", "Sales"]
cities = ["Karachi", "Lahore", "Islamabad", "Peshawar", "Quetta"]
genders = ["Male", "Female"]

data = {
    "Employee_ID":    [f"EMP{str(i).zfill(3)}" for i in range(1, n+1)],
    "Name":           [f"Employee_{i}" for i in range(1, n+1)],
    "Department":     np.random.choice(departments, n),
    "City":           np.random.choice(cities, n),
    "Gender":         np.random.choice(genders, n),
    "Age":            np.random.randint(22, 55, n).astype(float),
    "Salary":         np.random.randint(30000, 150000, n).astype(float),
    "Performance":    np.random.randint(50, 100, n).astype(float),
    "Experience_Yrs": np.random.randint(1, 20, n).astype(float),
    "Email":          [f"emp{i}@company.com" for i in range(1, n+1)],
}

df = pd.DataFrame(data)

# Introduce some mess
for col in ["Age", "Salary", "Performance"]:
    idx = np.random.choice(df.index, 5, replace=False)
    df.loc[idx, col] = np.nan

dup_rows = df.iloc[:3].copy()
df = pd.concat([df, dup_rows], ignore_index=True)

df.to_excel("sample_data.xlsx", index=False)
print(f"✅ sample_data.xlsx created  ({len(df)} rows, {len(df.columns)} cols)")
print(f"   Missing values: {df.isnull().sum().sum()}")
print(f"   Duplicate rows: {df.duplicated().sum()}")
