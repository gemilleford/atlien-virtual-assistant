import streamlit as st
import asyncio
import os
import nest_asyncio
from promptflow.core import AsyncFlow

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

# Load and parse the knowledge base (all files in the 'data' directory)
def load_knowledge_base(directory_path):
    """Load the knowledge base from all text files in the specified directory."""
    knowledge_base = {
        "landmarks": {},
        "government_services": {},
        "utilities": {}
    }
    
    # Loop through all files in the data directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        
        if filename.endswith(".txt"):
            try:
                with open(file_path, 'r') as f:
                    for line in f.readlines():
                        if ": " in line:
                            item, value = line.split(": ")
                            item, value = item.strip(), value.strip()
                            
                            # Categorize based on keywords
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

def search_knowledge_base(knowledge_base, query):
    """Search for a match in the knowledge base (landmarks, government services, utilities)."""
    query_lower = query.lower()

    # Exact match search
    for category, items in knowledge_base.items():
        for item, value in items.items():
            if query_lower in item.lower():
                return f"{item} ({category.capitalize()}) is located in: {value}."

    # Broad search based on keywords
    if "water" in query_lower:
        return knowledge_base["utilities"].get("Water Services", None)
    if "electricity" in query_lower or "power" in query_lower:
        return knowledge_base["utilities"].get("Electricity", None)
    if "natural gas" in query_lower:
        return knowledge_base["utilities"].get("Natural Gas", None)
    if "trash" in query_lower or "recycling" in query_lower:
        return knowledge_base["utilities"].get("Trash and Recycling", None)

    return None

async def run_flow(flow, prompt):
    """Run the flow asynchronously and return the final response."""
    result = await flow(
        chat_history=st.session_state.chat_history,
        question=prompt
    )

    # Collect the response from the async generator or result
    response = ""
    if isinstance(result['answer'], str):
        response = result['answer']
    elif isinstance(result['answer'], list):
        response = ''.join(result['answer'])
    else:
        async for res in result['answer']:
            response += res
    return response

def handle_user_input(flow, knowledge_base):
    """Handle user input, run the flow, and display the response."""
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        # Check if the user input relates to the knowledge base
        response = search_knowledge_base(knowledge_base, prompt)

        if not response:
            # If no response from the knowledge base, augment the OpenAI API request with knowledge base context
            utilities_context = " ".join([f"{k}: {v}" for k, v in knowledge_base["utilities"].items()])
            government_context = " ".join([f"{k}: {v}" for k, v in knowledge_base["government_services"].items()])

            # Build the prompt with knowledge base data as context
            final_prompt = f"Here is relevant information about utilities and government services in Atlanta:\nUtilities:\n{utilities_context}\nGovernment Services:\n{government_context}\nUser question: {prompt}"

            # Run the OpenAI API using the augmented prompt
            loop = asyncio.get_event_loop()
            final_result = loop.run_until_complete(run_flow(flow, final_prompt))

            # Display the assistant's response
            if final_result:
                st.session_state.messages.append({"role": "assistant", "content": final_result})
                st.session_state.chat_history.append({"role": "assistant", "content": final_result})
                with st.chat_message("assistant"):
                    st.markdown(final_result)
            else:
                st.error("No response received from the flow.")
        else:
            # If the knowledge base had a result, display it
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)

def display_title_and_description():
    """Display the app title and description."""
    st.title("🍑 ATLien Assistant")
    st.write(
        "Welcome to ATLien Assistant, an AI-powered virtual assistant designed "
        "to help newcomers and residents navigate the vibrant city of Atlanta. "
        "Whether you're searching for the best neighborhoods, local hotspots, "
        "or upcoming events, ATLien Assistant provides personalized insights "
        "and real-time information. With deep knowledge of the city’s culture, "
        "lifestyle, and opportunities, this assistant will guide you through "
        "everything from finding great restaurants to understanding transportation "
        "options—all at your fingertips."
    )

def initialize_session_state():
    """Initialize session state variables for messages, chat history, and first-time introduction."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "introduced" not in st.session_state:
        st.session_state.introduced = False  # Track whether the assistant has introduced itself

def introduce_assistant():
    """Introduce the ATLien Assistant with a focus on helping people transition to life in Atlanta."""
    if not st.session_state.introduced:
        intro_message = (
            "Hi, I'm ATLien Assistant! I'm here to provide you with the resources and information you need to quickly settle into life in Atlanta. "
            "Whether you're looking for great places to eat, fun spots to visit, family-friendly activities, or exciting local events, "
            "I'm here to make your transition as smooth and enjoyable as possible. Feel free to ask me anything about the city!"
        )
        st.session_state.messages.append({"role": "assistant", "content": intro_message})
        st.session_state.chat_history.append({"role": "assistant", "content": intro_message})
        st.session_state.introduced = True  # Set flag to avoid repeated introductions

def display_chat_messages():
    """Display existing chat messages stored in session state."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def main():
    """Main function to run the ATLien Assistant app."""
    display_title_and_description()

    openai_api_key = st.text_input("OpenAI API Key", type="password")
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.", icon="🗝️")
    else:
        os.environ["OPENAI_API_KEY"] = openai_api_key
        try:
            flow = AsyncFlow.load(source="./my_chatbot/flow.dag.yaml")
            initialize_session_state()

            # Load the knowledge base from the 'data' directory
            knowledge_base = load_knowledge_base("./data/")

            # Ensure the assistant introduces itself only once
            if not st.session_state.messages:
                introduce_assistant()

            # Display chat history and handle user input
            display_chat_messages()
            handle_user_input(flow, knowledge_base)
        except Exception as e:
            st.error(f"An error occurred while loading the flow: {e}")

if __name__ == "__main__":
    main()