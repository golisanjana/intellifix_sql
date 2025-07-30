import sqlparse

print("--- Analyzing SQL Queries with sqlparse ---")

# Correct query
query_correct = "SELECT name, age FROM users WHERE age > 25 ORDER BY name;"
print(f"\nOriginal Correct Query: {query_correct}")
parsed_correct = sqlparse.parse(query_correct)[0]
print("Tokens:")
for token in parsed_correct.tokens:
    if token.is_group: # Groups like parenthesis, identifier lists
        print(f"  Group: '{token.value}' Type: {token.ttype}")
        for sub_token in token.tokens:
            print(f"    Sub-token: '{sub_token.value}' Type: {sub_token.ttype}")
    else:
        print(f"  Token: '{token.value}' Type: {token.ttype}")

# Incorrect query 1: Misspelled keyword (SELET, WHRE)
query_incorrect_1 = "SELET name, age FROM users WHRE age > 25;"
print(f"\nOriginal Incorrect Query 1 (Misspelled): {query_incorrect_1}")
parsed_incorrect_1 = sqlparse.parse(query_incorrect_1)[0]
print("Tokens:")
for token in parsed_incorrect_1.tokens:
    if token.is_group:
        print(f"  Group: '{token.value}' Type: {token.ttype}")
        for sub_token in token.tokens:
            print(f"    Sub-token: '{sub_token.value}' Type: {sub_token.ttype}")
    else:
        print(f"  Token: '{token.value}' Type: {token.ttype}")

# Incorrect query 2: Missing FROM clause
query_incorrect_2 = "SELECT name, age users WHERE age > 25;"
print(f"\nOriginal Incorrect Query 2 (Missing FROM): {query_incorrect_2}")
parsed_incorrect_2 = sqlparse.parse(query_incorrect_2)[0]
print("Tokens:")
for token in parsed_incorrect_2.tokens:
    if token.is_group:
        print(f"  Group: '{token.value}' Type: {token.ttype}")
        for sub_token in token.tokens:
            print(f"    Sub-token: '{sub_token.value}' Type: {sub_token.ttype}")
    else:
        print(f"  Token: '{token.value}' Type: {token.ttype}")

# Incorrect query 3: Unbalanced Parentheses
query_incorrect_3 = "SELECT COUNT(id FROM orders;"
print(f"\nOriginal Incorrect Query 3 (Unbalanced Parentheses): {query_incorrect_3}")
parsed_incorrect_3 = sqlparse.parse(query_incorrect_3)[0]
print("Tokens:")
for token in parsed_incorrect_3.tokens:
    if token.is_group:
        print(f"  Group: '{token.value}' Type: {token.ttype}")
        for sub_token in token.tokens:
            print(f"    Sub-token: '{sub_token.value}' Type: {sub_token.ttype}")
    else:
        print(f"  Token: '{token.value}' Type: {token.ttype}")