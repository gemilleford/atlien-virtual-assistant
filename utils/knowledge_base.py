import json
import os
import streamlit as st

# Load and parse the knowledge base (all files in the 'data' directory)
def load_knowledge_base():
    """Load the knowledge base from the provided text files."""
    knowledge_base = {
        "landmarks": {},
        "government_services": {},
        "utilities": {},
        "restaurants": {}
    }

    knowledge_base_w_restaurants = load_restaurants(knowledge_base)

    full_knowledge_base = load_text_data(knowledge_base_w_restaurants)

    return full_knowledge_base

def load_text_data(knowledge_base):
    for filename in os.listdir("data/"):
        file_path = os.path.join("data/", filename)

        if filename.endswith(".txt"):
            try:
                with open(file_path, 'r') as f:
                    for line in f.readlines():
                        if ": " in line:
                            item, value = line.split(": ")
                            item, value = item.strip(), value.strip()

                            # Categorize based on keywords in the filenames
                            if "landmark" in filename:
                                knowledge_base["landmarks"][item] = value
                            elif "government" in filename:
                                knowledge_base["government_services"][item] = value
                            elif any(word in item.lower() for word in ["water", "electricity", "natural gas", "trash", "recycling"]):
                                knowledge_base["utilities"][item] = value
            except FileNotFoundError:
                st.error(f"Knowledge base file {file_path} not found.")
            except Exception as e:
                st.error(f"An error occurred while processing {file_path}: {e}")

    return knowledge_base


# Search the knowledge base for information
def search_knowledge_base(knowledge_base, query):
    """Search for a match in the knowledge base (landmarks, government services, utilities)."""
    query_lower = query.lower()

    # Search each category for a match
    for category, items in knowledge_base.items():
        for item, value in items.items():
            if query_lower in item.lower():
                return f"{item} ({category.capitalize()}) is located in: {value}."

    # If no direct match is found, search for utilities based on keywords
    for keyword in ["water", "electricity", "natural gas", "trash", "recycling"]:
        if keyword in query_lower:
            utility = knowledge_base["utilities"].get(keyword.capitalize(), None)
            if utility:
                return utility

    if "restaurant" in query_lower:
        return present(knowledge_base["restaurants"], query)

    return None  # No match found

def load_restaurants(knowledge_base):    
    with open('data/restaurants.json', 'r') as f:
        restaurants = json.load(f)
        for restaurant in restaurants:
            knowledge_base["restaurants"][restaurant["name"]] = restaurant

    return knowledge_base

def present(restaurants, query):
    response = ""
    types = []
    for restaurant in restaurants.values():
        type = restaurant['type']
        types += type
        if any(word in query for word in type):
            response += f"\n - {restaurant['description']}. \nIt can be found at {restaurant['address']}.\n"

    if not response:
        response = f"I can help you with these types of restaurants: {list(set(types))}"
    return response