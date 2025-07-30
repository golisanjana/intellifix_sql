import random
import pandas as pd
import os

# Ensure the datasets directory exists
os.makedirs('datasets', exist_ok=True)

def introduce_syntax_error(correct_sql: str) -> str:
    errors = [
        # Misspell common keywords
        lambda q: q.replace("SELECT", "SELET") if "SELECT" in q else q,
        lambda q: q.replace("FROM", "FRUM") if "FROM" in q else q,
        lambda q: q.replace("WHERE", "WHRE") if "WHERE" in q else q,
        lambda q: q.replace("GROUP BY", "GROPU BY") if "GROUP BY" in q else q,
        lambda q: q.replace("ORDER BY", "ORDR BY") if "ORDER BY" in q else q,
        lambda q: q.replace("JOIN", "JON") if "JOIN" in q else q,
        lambda q: q.replace("INSERT INTO", "INSRT INTO") if "INSERT INTO" in q else q,
        lambda q: q.replace("UPDATE", "UPDAT") if "UPDATE" in q else q,
        lambda q: q.replace("DELETE FROM", "DELET FROM") if "DELETE FROM" in q else q,

        # Remove common keywords/clauses (make it missing)
        lambda q: q.replace("FROM", "").strip() if "FROM" in q and "SELECT" in q else q,
        lambda q: q.replace("WHERE", "").strip() if "WHERE" in q else q,
        lambda q: q.replace("ORDER BY", "").strip() if "ORDER BY" in q else q,

        # Missing semicolon (if present)
        lambda q: q.replace(";", "") if q.endswith(";") else q,

        # Unbalanced parentheses (simple case)
        lambda q: q + "(" if random.random() < 0.5 else q + ")", # Add a random unclosed paren
    ]

    # Filter out errors that won't apply to the current query
    applicable_errors = [err for err in errors if err(correct_sql) != correct_sql]

    if not applicable_errors:
        return correct_sql # If no applicable errors, return original (or handle as needed)

    return random.choice(applicable_errors)(correct_sql)

# A diverse set of correct SQL queries
correct_queries = [
    "SELECT id, name, email FROM users WHERE age > 25 ORDER BY name;",
    "INSERT INTO products (name, price, stock) VALUES ('Laptop', 1200.00, 50);",
    "UPDATE orders SET status = 'shipped', ship_date = CURRENT_DATE WHERE order_id = 101;",
    "DELETE FROM customers WHERE last_activity < '2024-01-01';",
    "SELECT COUNT(DISTINCT department) FROM employees GROUP BY city HAVING COUNT(*) > 10;",
    "SELECT o.order_id, c.customer_name FROM orders o JOIN customers c ON o.customer_id = c.id WHERE o.order_date = '2025-07-28';",
    "CREATE TABLE temp_log (id INT PRIMARY KEY, message VARCHAR(255));",
    "ALTER TABLE users ADD COLUMN phone_number VARCHAR(20);",
    "DROP TABLE old_data;",
    "SELECT MAX(salary) AS max_salary, MIN(salary) AS min_salary FROM employees WHERE department = 'Sales';",
    "SELECT product_name FROM products WHERE price BETWEEN 100 AND 500;",
    "SELECT employee_id, first_name, last_name FROM employees WHERE employee_id IN (1, 5, 9);",
    "SELECT * FROM inventory ORDER BY quantity DESC LIMIT 10;",
    "SELECT AVG(rating) FROM reviews WHERE product_id = 789;",
    "CREATE INDEX idx_customer_email ON customers (email);"
]

dataset = []
num_errors_per_query = 5 # Generate 5 bad versions for each correct query

for query in correct_queries:
    for _ in range(num_errors_per_query):
        bad_query = introduce_syntax_error(query)
        # Ensure the bad query is actually different from the correct one
        if bad_query != query:
            dataset.append({"bad_sql": bad_query.strip(), "correct_sql": query.strip()})
        else:
            # If the random error didn't change it, try again or add a specific simple error
            if random.random() < 0.5: # 50% chance to add a missing semicolon if it was there
                if query.endswith(';'):
                    dataset.append({"bad_sql": query[:-1].strip(), "correct_sql": query.strip()})
            else: # 50% chance to misspell SELECT
                if "SELECT" in query:
                    dataset.append({"bad_sql": query.replace("SELECT", "SELET").strip(), "correct_sql": query.strip()})

df = pd.DataFrame(dataset)
output_file = "datasets/synthetic_sql_errors.csv"
df.to_csv(output_file, index=False)
print(f"Generated {len(df)} SQL error pairs to {output_file}")

# Display a few examples
print("\n--- Sample Generated Data ---")
print(df.head())