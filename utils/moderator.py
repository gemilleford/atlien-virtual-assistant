import json
import streamlit as st
from better_profanity import profanity
from utils.allow_list import allow_list

# Initialize the better-profanity filter with custom allow list
profanity.load_censor_words(whitelist_words=allow_list)

def moderate(user_input):
    """Moderate input for profanity using better-profanity."""

    if profanity.contains_profanity(user_input):
        # Warn of and censor the profanity in the text
        st.warning("Your input contained inappropriate language and has been censored.")

        user_input = profanity.censor(user_input)

    return neutralize_prompt(user_input)

def check_for_sensitive_topic(user_query):
    sensitive_topics = load_json('data/sensitive_topics.json')
    """Check if the query involves sensitive topics."""
    for topic in sensitive_topics:
        if topic in user_query.lower():
            return sensitive_topics[topic]
    return None

def neutralize_prompt(user_query):
    """Neutralize potentially biased queries."""
    if "best neighborhood" in user_query.lower():
        return "Can you provide a list of neighborhoods in Atlanta and what they are known for?"
    return user_query

def load_json(file_path):
    """Load data from a JSON file."""
    data = {}
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        st.error(f"JSON file {file_path} not found.")
    return data