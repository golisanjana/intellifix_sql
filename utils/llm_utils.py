# File: utils/llm_utils.py (Final corrected Hugging Face version)
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import json

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise ValueError("HF_TOKEN not found in .env file. Please get one from Hugging Face.")

# The Hugging Face client allows us to call a model
client = InferenceClient(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    token=HF_TOKEN
)

def fix_sql_with_llm(bad_sql: str, schema: dict = None) -> str:
    """
    Sends a broken SQL query and an optional schema to an LLM and returns the corrected version.
    """
    # Create a system message and a user message for a chat-like interaction
    messages = [
        {"role": "system", "content": "You are a helpful SQL assistant. Your task is to fix any syntax or logical errors in the provided SQL query. Respond with ONLY the corrected SQL query, nothing else."},
        {"role": "user", "content": f"Broken SQL:\n{bad_sql}"}
    ]
    
    # If a schema is provided, we add it to the user message
    if schema:
        schema_string = json.dumps(schema, indent=2)
        messages[1]["content"] = f"The database schema is as follows:\n{schema_string}\n\n{messages[1]['content']}"

    try:
        # Use a chat-based method to call the model
        response = client.chat_completion(
            messages=messages,
            max_tokens=200,
        )
        
        corrected_sql = response.choices[0].message.content.strip()
        
        # Clean up any markdown code blocks
        if corrected_sql.startswith("```sql") and corrected_sql.endswith("```"):
            corrected_sql = corrected_sql[6:-3].strip()
        elif corrected_sql.startswith("```") and corrected_sql.endswith("```"):
            corrected_sql = corrected_sql[3:-3].strip()
        
        return corrected_sql
    except Exception as e:
        print(f"Error calling LLM: {e}")
        return f"Error: Could not fix query. {e}"

# --- For local testing ---
if __name__ == "__main__":
    test_query_with_schema = "SELECT username FROM usrs;" # "usrs" is a typo
    sample_schema = {
        "users": ["user_id", "username", "email"],
        "products": ["product_id", "product_name", "price"]
    }
    fixed_with_schema = fix_sql_with_llm(test_query_with_schema, schema=sample_schema)
    print(f"Test 2 (With Schema) - Original: {test_query_with_schema}")
    print(f"Test 2 (With Schema) - Fixed: {fixed_with_schema}")