import sqlite3
import yaml
import os

# Load YAML
with open("responses/health_responses.yaml", "r") as f:
    data = yaml.safe_load(f)
    responses = data["responses"]

# Make sure 'data' folder exists
os.makedirs("data", exist_ok=True)

# Connect to SQLite DB
conn = sqlite3.connect("data/health_responses.db")
c = conn.cursor()

# Create table with keywords column
c.execute("""
CREATE TABLE IF NOT EXISTS responses (
    intent TEXT PRIMARY KEY,
    keywords TEXT,
    question TEXT,
    answer TEXT,
    disclaimer TEXT
)
""")

# Insert data from YAML
for r in responses:
    keywords = ",".join(r.get("keywords", []))  # join list into CSV string
    c.execute("INSERT OR REPLACE INTO responses VALUES (?, ?, ?, ?, ?)",
              (r["intent"], keywords, r["question"], r["answer"], r["disclaimer"]))

conn.commit()
conn.close()

print("Database initialized at data/health_responses.db")
