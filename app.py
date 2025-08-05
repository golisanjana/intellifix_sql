import streamlit as st
from utils.llm_utils import fix_sql_with_llm
from utils.sql_utils import is_valid_sql_syntax
from utils.schema_utils import parse_schema_from_ddl
import json
import os

st.set_page_config(page_title="IntelliFixSQL", layout="centered")

st.title("💡 IntelliFixSQL: AI-Powered SQL Query Corrector")

st.markdown("""
Enter your SQL query below, and I'll try to fix any errors and explain the changes.
""")

# --- Schema Upload UI ---
st.sidebar.header("Database Schema")
uploaded_schema_file = st.sidebar.file_uploader("Upload your database schema (.sql file)", type=["sql"])

# Store parsed schema in session state
if 'parsed_schema' not in st.session_state:
    st.session_state.parsed_schema = None

schema_string = ""
if uploaded_schema_file is not None:
    schema_string = uploaded_schema_file.read().decode("utf-8")
    st.session_state.parsed_schema = parse_schema_from_ddl(schema_string)
    if st.session_state.parsed_schema:
        st.sidebar.success(f"Schema uploaded with {len(st.session_state.parsed_schema)} tables.")
        st.sidebar.markdown("**Schema Preview:**")
        st.sidebar.json(st.session_state.parsed_schema)
    else:
        st.sidebar.error("Could not parse schema file. Please check syntax.")

# --- Main UI Logic ---
user_sql_input = st.text_area("Enter your SQL query here:", height=200, placeholder="e.g., SELET * FROM users WHRE age > 30;", key="sql_input_area")

if st.button("✨ Fix Query"):
    if not user_sql_input:
        st.warning("Please enter a SQL query to fix.")
    else:
        with st.spinner("Analyzing and fixing your query..."):\
            corrected_sql = fix_sql_with_llm(user_sql_input, schema=st.session_state.parsed_schema)

        st.subheader("✅ Corrected SQL Query:")
        st.code(corrected_sql, language="sql")

            # Validate corrected SQL
        is_valid = is_valid_sql_syntax(corrected_sql)
        if is_valid:
                st.success("Syntax Check: The corrected query appears to be syntactically valid!")
        else:
                st.error("Syntax Check: The corrected query still has syntax issues. Please review.")

            # (Optional) Get explanation from LLM
        st.subheader("🧠 Explanation of Fixes:")
        explanation_prompt_content = ""
        try:
                with open("prompts/explain_fix_prompt.txt", "r") as f:
                    explanation_prompt_content = f.read()
        except FileNotFoundError:
                explanation_prompt_content = "You are a helpful SQL assistant. Explain the errors in the original SQL query and how they were fixed in the corrected version. Be concise and clear. Focus only on the SQL syntax and logical changes."

        explanation_prompt = f"""
            {explanation_prompt_content}

            Original SQL:
            {user_sql_input}

            Corrected SQL:
            {corrected_sql}

            Explanation:
            """
        try:
                # This is a bit advanced: we will reuse the main LLM call for explanation
                explanation = fix_sql_with_llm(explanation_prompt)
                st.info(explanation)
        except Exception as e:
                st.warning(f"Could not generate explanation: {e}")

# Note: I have removed the sample queries and feedback logging for this simplified example, but you can add them back later.
else:
        st.sidebar.error("Could not parse schema file. Please check syntax.")

# --- Existing UI logic (from your MVP) ---
# Use st.session_state for persistent input across reruns
if 'user_sql_input_display' not in st.session_state:
    st.session_state.user_sql_input_display = ""

user_sql_input = st.text_area("Enter your SQL query here:", height=200, placeholder="e.g., SELET * FROM users WHRE age > 30;", value=st.session_state.user_sql_input_display, key="sql_input_area")

# Fix Query Button
if st.button("✨ Fix Query"):
    # We will integrate the schema logic here in the next step
    if not user_sql_input:
        st.warning("Please enter a SQL query to fix.")
    else:
        st.session_state.user_sql_input_display = user_sql_input

        with st.spinner("Analyzing and fixing your query..."):
            # 1. Get corrected SQL from LLM (without schema yet)
            corrected_sql = fix_sql_with_llm(user_sql_input)

            st.subheader("✅ Corrected SQL Query:")
            st.code(corrected_sql, language="sql")

            # 2. Validate corrected SQL
            is_valid = is_valid_sql_syntax(corrected_sql)
            if is_valid:
                st.success("Syntax Check: The corrected query appears to be syntactically valid!")
            else:
                st.error("Syntax Check: The corrected query still has syntax issues. Please review.")

            # 3. (Optional) Get explanation from LLM
            st.subheader("🧠 Explanation of Fixes:")
            explanation_prompt_content = ""
            try:
                with open("prompts/explain_fix_prompt.txt", "r") as f:
                    explanation_prompt_content = f.read()
            except FileNotFoundError:
                explanation_prompt_content = "You are a helpful SQL assistant. Explain the errors in the original SQL query and how they were fixed in the corrected version. Be concise and clear. Focus only on the SQL syntax and logical changes."

            explanation_prompt = f"""
            {explanation_prompt_content}

            Original SQL:
            {user_sql_input}

            Corrected SQL:
            {corrected_sql}

            Explanation:
            """
            try:
                explanation = fix_sql_with_llm(explanation_prompt) # Reusing the fix function for explanation
                st.info(explanation)
            except Exception as e:
                st.warning(f"Could not generate explanation: {e}")

# Add session state to store previous results for feedback logging
# This part is for feedback logging from Phase 1, you can keep it as is
if 'corrected_sql' in locals():
    st.session_state.corrected_sql_display = corrected_sql
    st.session_state.original_sql_display = user_sql_input
else:
    st.session_state.corrected_sql_display = ""
    st.session_state.original_sql_display = ""