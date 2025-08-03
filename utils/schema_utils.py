# File: utils/schema_utils.py (Final corrected version with bug fix)
# File: utils/schema_utils.py (Final corrected version)
import sqlglot
from sqlglot.errors import ParseError

def parse_schema_from_ddl(ddl_content: str) -> dict:
    """
    Parses SQL DDL (CREATE TABLE statements) and extracts a dictionary
    of table names and their columns.
    
    Args:
        ddl_content: A string containing one or more CREATE TABLE statements.
        
    Returns:
        A dictionary where keys are table names and values are a list of column names.
    """
    schema = {}
    try:
        expressions = sqlglot.parse(ddl_content, read="postgres")
        for exp in expressions:
            if isinstance(exp, sqlglot.exp.Create):
                table_exp = exp.find(sqlglot.exp.Table)
                if table_exp:
                    table_name = table_exp.name
                    # Find the schema expression to get columns
                    schema_exp = exp.find(sqlglot.exp.Schema)
                    if schema_exp:
                        columns = []
                        for column_exp in schema_exp.args.get("expressions", []):
                            # The column name is the first part of the expression
                            if isinstance(column_exp, sqlglot.exp.ColumnDef):
                                columns.append(column_exp.name)
                        schema[table_name] = columns
    except ParseError as e:
        print(f"Error parsing DDL: {e}")
        return {}
    
    return schema

# --- For local testing ---
if __name__ == "__main__":
    sample_ddl = """
    CREATE TABLE users (
      user_id INT PRIMARY KEY,
      user_name VARCHAR(255) NOT NULL,
      email VARCHAR(255) UNIQUE
    );
    
    CREATE TABLE products (
      product_id INT PRIMARY KEY,
      product_name VARCHAR(255) NOT NULL,
      price DECIMAL(10, 2),
      category_id INT
    );
    """
    
    parsed_schema = parse_schema_from_ddl(sample_ddl)
    print("Parsed Schema:")
    print(parsed_schema)