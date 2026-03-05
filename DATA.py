import pandas as pd
import numpy as np

np.random.seed(42)

rows = 1000

data = {
    "CGPA": np.round(np.random.uniform(5.0, 9.8, rows), 2),
    "10th_Percentage": np.random.randint(50, 95, rows),
    "12th_Percentage": np.random.randint(50, 95, rows),
    "Internship": np.random.randint(0, 2, rows),
    "Projects": np.random.randint(0, 6, rows),
    "Aptitude_Score": np.random.randint(40, 100, rows),
    "Communication_Skill": np.random.randint(1, 10, rows)
}

df = pd.DataFrame(data)

# Placement Logic
df["Placed"] = (
    (df["CGPA"] > 7.0) &
    (df["Aptitude_Score"] > 60) &
    (df["Communication_Skill"] > 5)
).astype(int)

df.to_csv("placement_dataset.csv", index=False)

print("Dataset Generated Successfully ✅")
print(df.head())