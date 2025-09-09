import sqlite3
import yaml
import os

# Load YAML responses
with open("responses/health_responses.yaml", "r") as f:  # always relative to project root
    data = yaml.safe_load(f)
    responses = data["responses"]

# Ensure 'data' folder exists
os.makedirs("data", exist_ok=True)

# Connect to SQLite DB inside 'data' folder
conn = sqlite3.connect("data/health_responses.db")
c = conn.cursor()

# Create table
c.execute("""
CREATE TABLE IF NOT EXISTS responses (
    intent TEXT PRIMARY KEY,
    answer TEXT,
    disclaimer TEXT
)
""")

# Insert responses
for r in responses:
    c.execute("INSERT OR REPLACE INTO responses VALUES (?, ?, ?)",
              (r["intent"], r["answer"], r["disclaimer"]))

conn.commit()
conn.close()
print("Database initialized at data/health_responses.db")
