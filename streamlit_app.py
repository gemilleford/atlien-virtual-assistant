import streamlit as st
import asyncio
from promptflow.core import AsyncFlow

# Show title and description.
st.title("🍑 ATLien Assistant")
st.write(
    "Welcome to ATLien Assistant, an AI-powered virtual assistant designed to help newcomers and residents navigate the vibrant city of Atlanta. "
    "Whether you're searching for the best neighborhoods, local hotspots, or upcoming events, ATLien Assistant provides personalized insights and real-time information. "
    "With deep knowledge of the city’s culture, lifestyle, and opportunities, this assistant will guide you through everything from finding great restaurants to understanding transportation options—all at your fingertips."
)

# Ask user for their OpenAI API key via `st.text_input`.
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Load the PromptFlow AsyncFlow object
    flow = AsyncFlow.load(source="./my_chatbot/flow.dag.yaml")

    # Create a session state variable to store the chat messages and chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Define an async function to run the flow and retrieve the actual answer
        async def run_flow():
            # Call the flow and capture the async generator
            result = await flow(
                chat_history=st.session_state.chat_history,  # Pass chat history
                question=prompt  # Pass the user input
            )
            
            # Iterate over the async generator to retrieve the final response
            response = ""
            async for res in result['answer']:
                response += res
            return response

        # Run the async flow function
        final_result = asyncio.run(run_flow())

        # Display and store the assistant's response in session state
        if final_result:
            st.session_state.messages.append({"role": "assistant", "content": final_result})
            st.session_state.chat_history.append({"role": "assistant", "content": final_result})
            with st.chat_message("assistant"):
                st.markdown(final_result)
        else:
            st.error("No response received from the flow.")