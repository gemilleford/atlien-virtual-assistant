### **Brand Voice in ATLien Assistant**

Creating a strong **Brand Voice** ensures that **ATLien Assistant** consistently communicates with users in a friendly, helpful, and knowledgeable tone, embodying the vibrant culture of Atlanta. In this section, we’ll discuss how to define and implement this voice throughout the assistant’s responses and interactions, including the use of **Jinja2** templates to maintain that consistency.

---

### **Defining the Brand Voice**

The **ATLien Assistant** is meant to be approachable, welcoming, and informative. The tone should balance professionalism with warmth, providing users with local insights while making them feel comfortable. Here’s how to define this voice in practice:

1. **Friendly and Conversational**: Responses should feel like they’re coming from a helpful local, making the user feel at home. Avoid overly formal language.
2. **Knowledgeable and Resourceful**: The assistant should be confident in providing accurate information, offering relevant suggestions and guidance.
3. **Welcoming and Inclusive**: The assistant should create an inviting atmosphere, particularly for newcomers to Atlanta, by offering personalized and empathetic responses.

#### **Brand Voice Examples**:
- **Introduction**: 
   - *"Hi, I'm ATLien Assistant! I'm here to provide you with the resources and information you need to quickly settle into life in Atlanta. Whether you're looking for great places to eat, fun spots to visit, family-friendly activities, or exciting local events, I'm here to make your transition as smooth and enjoyable as possible."*
- **Answering a Query**: 
   - *"Atlanta has so much to offer! If you're looking for local hotspots, I recommend checking out Piedmont Park or exploring the BeltLine. Would you like more suggestions?"*

---

### **Implementing Brand Voice with Jinja2 Templates**

To keep responses consistent with your brand voice, you can use **Jinja2** templates. **Jinja2** is a templating engine for Python, allowing you to insert dynamic data into pre-defined templates while maintaining the desired tone.

#### **How Jinja2 Works in the App**:
1. **Jinja2 Templates**: Templates define the structure of your responses while leaving placeholders for dynamic data (e.g., user queries or results from the knowledge base).
2. **Rendering Templates**: When the user interacts with the assistant, the dynamic parts of the conversation (e.g., user input) are inserted into the template, ensuring that the responses are always consistent with the brand voice.

---

### **Using Jinja2 in ATLien Assistant**

1. **Define a Jinja2 Template**: Create a `.jinja2` file for a friendly introduction or response. For example, you might create `introduction.jinja2` to standardize how the assistant introduces itself.

Here’s what a **Jinja2** template for the assistant’s introduction might look like:

```jinja2
{% block intro %}
Hi, I'm ATLien Assistant! I'm here to help you settle into Atlanta. Whether you're looking for {{ suggestion_type }}, or need tips about {{ advice_type }}, I've got you covered! How can I assist you today?
{% endblock %}
```

This template includes placeholders for dynamic data like `suggestion_type` (e.g., "local restaurants") and `advice_type` (e.g., "transportation options"). 

2. **Render the Jinja2 Template in the App**: Use the `jinja2` library to render templates with dynamic data. When the assistant needs to introduce itself or provide a response, it inserts the relevant data into the placeholders.

Here’s how you can render a **Jinja2** template in the **ATLien Assistant**:

```python
from jinja2 import Environment, FileSystemLoader

# Load the Jinja2 environment and templates directory
env = Environment(loader=FileSystemLoader('templates'))

def render_intro(suggestion_type, advice_type):
    """Render the introduction template with dynamic values."""
    template = env.get_template('introduction.jinja2')
    return template.render(suggestion_type=suggestion_type, advice_type=advice_type)

# Example usage
intro_message = render_intro("great places to eat", "public transportation")
print(intro_message)
```

3. **Structure Responses Using Templates**: Jinja2 templates can be used not only for introductions but also for responses based on user queries. For example, if a user asks about parks, a **Jinja2** template can generate a response that integrates the user's query while keeping the brand voice intact.

---

### **Integrating Jinja2 Templates in the App Workflow**

To integrate **Jinja2** with **Streamlit**, you’ll load the templates, render them based on user input, and display the final, branded response in the chat window.

#### **Steps to Integrate Jinja2**:

1. **Set up a Templates Directory**:
   - Create a `templates` folder in your project to store the **Jinja2** files (e.g., `introduction.jinja2`, `response.jinja2`).

2. **Render Templates in the App**:
   - When handling user input or generating responses from the knowledge base, render the response using a **Jinja2** template to ensure it maintains the brand voice.

3. **Display the Rendered Response in Streamlit**:
   - Once the template is rendered, display it in the chat window using **Streamlit**’s interface.

```python
def handle_user_input(flow, knowledge_base):
    if prompt := st.chat_input("Ask me anything about Atlanta!"):
        # Moderate input and search the knowledge base as usual
        cleaned_prompt, is_profane = moderate_user_input(prompt)

        # Example of using Jinja2 to render a response
        intro_message = render_intro("fun spots", "local events")
        
        # Display the assistant's response
        st.session_state.messages.append({"role": "assistant", "content": intro_message})
        st.session_state.chat_history.append({"role": "assistant", "content": intro_message})
        with st.chat_message("assistant"):
            st.markdown(intro_message)
```

---

### **Best Practices for Brand Voice with Jinja2**:
- **Keep Responses Friendly**: Ensure all templates reflect the tone of the ATLien Assistant—friendly, welcoming, and helpful.
- **Use Dynamic Data**: Personalize responses with the user’s query while maintaining the assistant’s brand voice using placeholders.
- **Consistent Structure**: Use **Jinja2** templates for recurring responses like introductions, fallback answers, and general information to ensure consistency throughout the user experience.

---

### **Conclusion: Maintaining Brand Voice Through Templates**

By integrating **Jinja2** templates with your app, you can ensure that every response from **ATLien Assistant** is consistent, friendly, and on-brand. Whether you’re introducing the assistant or providing answers from the knowledge base, templates allow you to control the structure and tone of responses while dynamically adapting to user input.

In the next steps, you can continue building the assistant by combining this brand voice with knowledge base queries and ensuring that responses from different sources (AI or knowledge base) are seamlessly blended into the conversation, maintaining a consistent user experience.