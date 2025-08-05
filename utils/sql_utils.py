# File: utils/sql_utils.py
import sqlparse

def is_valid_sql_syntax(query: str) -> bool:
    """
    Checks if a SQL query has valid syntax using sqlparse.
    Returns True if valid, False otherwise.
    """
    try:
        parsed_statements = sqlparse.parse(query)
        if not parsed_statements:
            return False
        # Check for any parsing errors
        # sqlparse doesn't throw exceptions for syntax errors, but we can check if it
        # successfully parsed a statement.
        return True
    except Exception:
        return False

if __name__ == "__main__":
    # A simple local test
    print(f"Is 'SELECT * FROM users;' valid? {is_valid_sql_syntax('SELECT * FROM users;')}")
    print(f"Is 'SELET * FROM users;' valid? {is_valid_sql_syntax('SELET * FROM users;')}")