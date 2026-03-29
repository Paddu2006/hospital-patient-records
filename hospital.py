# Hospital Patient Records Database
# By Padma Shree
# Project 4 of 25

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Step 1 - Create database
print("=== HOSPITAL PATIENT RECORDS ===")
conn = sqlite3.connect("hospital.db")
cursor = conn.cursor()

# Step 2 - Create patients table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER,
        gender TEXT,
        disease TEXT,
        admission_date TEXT,
        discharge_date TEXT,
        cost INTEGER
    )
""")

# Step 3 - Insert patient records
patients = [
    (1, "Rahul Sharma", 45, "Male", "Diabetes", "2024-01-05", "2024-01-15", 25000),
    (2, "Priya Singh", 32, "Female", "Hypertension", "2024-01-08", "2024-01-12", 18000),
    (3, "Amit Kumar", 67, "Male", "Heart Disease", "2024-01-10", "2024-01-25", 85000),
    (4, "Sunita Devi", 28, "Female", "Diabetes", "2024-01-15", "2024-01-20", 22000),
    (5, "Rajesh Patel", 55, "Male", "Hypertension", "2024-01-18", "2024-01-22", 15000),
    (6, "Meera Nair", 41, "Female", "Asthma", "2024-01-20", "2024-01-25", 12000),
    (7, "Vikram Rao", 73, "Male", "Heart Disease", "2024-01-22", "2024-02-05", 95000),
    (8, "Anita Joshi", 36, "Female", "Asthma", "2024-01-25", "2024-01-28", 10000),
    (9, "Suresh Menon", 62, "Male", "Diabetes", "2024-02-01", "2024-02-10", 28000),
    (10, "Kavitha Reddy", 49, "Female", "Heart Disease", "2024-02-05", "2024-02-18", 78000)
]

cursor.executemany("INSERT OR IGNORE INTO patients VALUES (?,?,?,?,?,?,?,?)", patients)
conn.commit()

# Step 4 - Query the database
print("\nAll patients:")
df = pd.read_sql_query("SELECT * FROM patients", conn)
print(df)

# Step 5 - Analysis
print("\n=== DISEASE ANALYSIS ===")
disease_df = pd.read_sql_query("""
    SELECT disease,
           COUNT(*) as total_patients,
           AVG(age) as avg_age,
           AVG(cost) as avg_cost
    FROM patients
    GROUP BY disease
    ORDER BY total_patients DESC
""", conn)
print(disease_df)

print("\n=== COST ANALYSIS ===")
print("Total hospital revenue: Rs.", df["cost"].sum())
print("Average treatment cost: Rs.", round(df["cost"].mean(), 2))
print("Most expensive treatment: Rs.", df["cost"].max())

# Step 6 - Charts
disease_count = pd.read_sql_query("""
    SELECT disease, COUNT(*) as total
    FROM patients
    GROUP BY disease
""", conn)

disease_count.plot(kind="bar", x="disease", y="total",
                   color="red", figsize=(10,6), legend=False)
plt.title("Patient Distribution by Disease")
plt.xlabel("Disease")
plt.ylabel("Number of Patients")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(r"C:\Users\Padma shree jena\Desktop\PadduDS_Journey\02_phase2\hospital_db\disease_distribution.png")
plt.show()
print("Chart 1 saved!!")

disease_df.plot(kind="bar", x="disease", y="avg_cost",
                color="blue", figsize=(10,6), legend=False)
plt.title("Average Treatment Cost by Disease")
plt.xlabel("Disease")
plt.ylabel("Average Cost (Rs.)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(r"C:\Users\Padma shree jena\Desktop\PadduDS_Journey\02_phase2\hospital_db\treatment_cost.png")
plt.show()
print("Chart 2 saved!!")

# Close database LAST
conn.close()
print("\nDatabase closed successfully!")