import streamlit as st
import os
import httpx
import nest_asyncio
from utils.restaurants import *
from utils.moderator import *

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

# Load and parse the knowledge base (all files in the 'data' directory)
def load_knowledge_base(directory_path):
    """Load the knowledge base from the provided text files."""
    knowledge_base = {
        "landmarks": {},
        "government_services": {},
        "utilities": {},
        "restaurants": {}
    }

    knowledge_base = load_restaurants(knowledge_base)

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        
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

    # If no direct match is found, check for utilities based on keywords
    if "water" in query_lower:
        return knowledge_base["utilities"].get("Water Services", None)
    if "electricity" in query_lower or "power" in query_lower:
        return knowledge_base["utilities"].get("Electricity", None)
    if "natural gas" in query_lower:
        return knowledge_base["utilities"].get("Natural Gas", None)
    if "trash" in query_lower or "recycling" in query_lower:
        return knowledge_base["utilities"].get("Trash and Recycling", None)
    if "restaurant" in query_lower:
        return present(knowledge_base["restaurants"], query)

    return None  # No match found

# Fetch response from Ollama if the knowledge base doesn't have the answer
def fetch_from_ollama(prompt, knowledge_base):
    """Send a request to the local Ollama instance running the Phi-3 model."""
    url = "http://localhost:11434/api/chat"

    # Prepare the context from the knowledge base to include in the prompt
    utilities_context = " ".join([f"{k}: {v}" for k, v in knowledge_base["utilities"].items()])
    government_context = " ".join([f"{k}: {v}" for k, v in knowledge_base["government_services"].items()])

    # Augment the prompt with context from the knowledge base
    full_prompt = f"""
    Here is relevant information about utilities and government services in Atlanta:
    Utilities:
    {utilities_context}

    Government Services:
    {government_context}

    User question: {prompt}
    """

    payload = {
        "model": "phi3",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": full_prompt}
        ],
        "stream": False
    }

    try:
        response = httpx.post(url, json=payload, timeout=300.0)  # Max out the timeout to 300 seconds
        response.raise_for_status()

        # Parse the entire response in one go rather than line-by-line
        try:
            json_response = response.json()

            # Check if the response has content
            if "message" in json_response and "content" in json_response["message"]:
                return json_response["message"]["content"]
            else:
                return "No response content received."

        except ValueError as e:
            st.error(f"Error parsing JSON response: {e}")
            return "Error processing the response from Ollama."

    except httpx.RequestError as e:
        st.error(f"An error occurred while making a request to Ollama: {e}")
        return "Error communicating with the local Ollama instance."
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return "Unexpected error while fetching response."

# Handle user input
def handle_user_input(knowledge_base):
    """Handle user input, first check the knowledge base, then Ollama if necessary."""
    # Input field for user queries
    user_input = st.chat_input("Ask me something about Atlanta:")

    # Process the input when the user submits
    if user_input:
        cleaned_and_neutralized_input = moderate(user_input)
        # Display user input immediately before fetching response
        st.session_state.messages.append({"role": "user", "content": cleaned_and_neutralized_input})
        with st.chat_message("user"):
            st.markdown(cleaned_and_neutralized_input)

        # Check if the user input relates to the knowledge base
        response = search_knowledge_base(knowledge_base, cleaned_and_neutralized_input)

        if response:
            # Respond from the knowledge base
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)
        else:
            # If no response from the knowledge base, call Ollama
            response = fetch_from_ollama(user_input, knowledge_base)
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)

# Display the app title and description
def display_title_and_description():
    """Display the app title and description."""
    st.title("🍑 ATLien Assistant")
    st.write(
        "Welcome to ATLien Assistant, an AI-powered virtual assistant designed "
        "to help newcomers and residents navigate the vibrant city of Atlanta. "
    )

# Initialize session state
def initialize_session_state():
    """Initialize session state variables for messages, chat history, and first-time introduction."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "introduced" not in st.session_state:
        st.session_state.introduced = False  # Track whether the assistant has introduced itself

# Introduce the assistant
def introduce_assistant():
    """Introduce the ATLien Assistant."""
    if not st.session_state.introduced:
        intro_message = (
            "Hi, I'm ATLien Assistant! I'm here to provide you with the resources and information you need to quickly settle into life in Atlanta. "
            "Whether you're looking for great places to eat, fun spots to visit, family-friendly activities, or exciting local events, "
            "I'm here to make your transition as smooth and enjoyable as possible. Feel free to ask me anything about the city!"
        )
        st.session_state.messages.append({"role": "assistant", "content": intro_message})
        st.session_state.chat_history.append({"role": "assistant", "content": intro_message})
        st.session_state.introduced = True  # Set flag to avoid repeated introductions

# Display chat history
def display_chat_messages():
    """Display existing chat messages stored in session state."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Main function to run the ATLien Assistant app
def main():
    """Main function to run the ATLien Assistant app."""
    display_title_and_description()
    initialize_session_state()

    # Load the knowledge base from the 'data' directory
    knowledge_base = load_knowledge_base("./data/")

    # Ensure the assistant introduces itself only once
    if not st.session_state.messages:
        introduce_assistant()

    # Display chat history and handle user input
    display_chat_messages()
    handle_user_input(knowledge_base)

if __name__ == "__main__":
    main()