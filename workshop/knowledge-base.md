### **Knowledge Base in ATLien Assistant**

The **ATLien Assistant** relies on a robust knowledge base to provide accurate, localized responses. In addition to AI-powered responses, the assistant taps into structured data stored in **TXT**, **CSV**, and **JSON** formats to ensure it provides reliable and contextually relevant information for Atlanta residents and newcomers. Importantly, we also augment the AI model's responses with data from the knowledge base to enhance accuracy.

This section will cover how to load data from various file formats into the knowledge base, as well as how to parse this data through the AI model for optimal performance.

---

### **Supported Data Points and File Formats**

Here are the additional data points that will be integrated into the knowledge base, using a variety of file formats:

1. **Transportation Options** - CSV, TXT
2. **Schools and Education** - JSON, TXT
3. **Healthcare Facilities** - CSV, TXT
4. **Events and Entertainment** - JSON, TXT
5. **Emergency Services** - CSV, TXT

The knowledge base will pull this data and then ensure it’s available to the assistant for both direct responses and augmented AI model responses.

---

### **Integrating TXT, CSV, and JSON Files into the Knowledge Base**

We will extend the current codebase to load data from **CSV**, **JSON**, and **TXT** files while ensuring that this data is also used to augment the prompts sent to the AI model. Here's how you can load data from these formats and integrate it into the knowledge base.

---

### **1. Loading Data from CSV Files**

**Example CSV File (`transport.csv`)**:
```csv
mode,provider,contact
Bus,MARTA,404-848-5000
Train,MARTA,404-848-5000
Rideshare,Uber/Lyft,N/A
```

**Loading CSV Data into the Knowledge Base**:
```python
import csv

def load_knowledge_base_from_csv(file_path):
    """Load transportation options from a CSV file."""
    data = {}
    try:
        with open(file_path, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                data[row['mode']] = {
                    'provider': row['provider'],
                    'contact': row['contact']
                }
    except FileNotFoundError:
        st.error(f"CSV file {file_path} not found.")
    return data
```

---

### **2. Loading Data from JSON Files**

**Example JSON File (`schools.json`)**:
```json
{
  "Georgia Tech": {
    "type": "University",
    "location": "North Ave NW, Atlanta, GA",
    "rating": 4.9
  },
  "Atlanta International School": {
    "type": "K-12",
    "location": "2890 North Fulton Dr NE, Atlanta, GA",
    "rating": 4.7
  }
}
```

**Loading JSON Data into the Knowledge Base**:
```python
import json

def load_knowledge_base_from_json(file_path):
    """Load school data from a JSON file."""
    data = {}
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        st.error(f"JSON file {file_path} not found.")
    return data
```

---

### **3. Loading Data from TXT Files**

We can continue using the existing method to load **TXT** files for categories such as **events**, **healthcare**, and **emergency services**.

**Example TXT File (`events.txt`)**:
```txt
Music Midtown: September 17-19, Piedmont Park, Music Festival
Atlanta Food and Wine Festival: October 14-17, Midtown, Food Festival
```

**Loading TXT Data into the Knowledge Base**:
```python
def load_events_from_txt(file_path):
    """Load events data from a TXT file."""
    events = {}
    try:
        with open(file_path, 'r') as file:
            for line in file.readlines():
                if ": " in line:
                    event_name, details = line.split(": ")
                    events[event_name.strip()] = details.strip()
    except FileNotFoundError:
        st.error(f"TXT file {file_path} not found.")
    return events
```

---

### **4. Unified Knowledge Base Loader**

Now we’ll combine all the functions into a unified loader that can handle all the file formats and store the data in the knowledge base. We will make sure this data can be parsed and passed into the AI model for enhanced responses.

```python
def load_complete_knowledge_base(directory_path, csv_transport, json_schools, csv_healthcare, json_events, csv_emergency):
    """Load the complete knowledge base from TXT, CSV, and JSON files."""
    knowledge_base = {
        "landmarks": {},  # Already covered
        "government_services": {},  # Already covered
        "utilities": {},  # Already covered
        "transportation": {},
        "schools": {},
        "healthcare": {},
        "events": {},
        "emergency_services": {}
    }

    # Load data from TXT files
    knowledge_base.update(load_knowledge_base(directory_path))  # Loading existing TXT data

    # Load additional data from CSV and JSON files
    knowledge_base["transportation"].update(load_knowledge_base_from_csv(csv_transport))
    knowledge_base["schools"].update(load_knowledge_base_from_json(json_schools))
    knowledge_base["healthcare"].update(load_knowledge_base_from_csv(csv_healthcare))
    knowledge_base["events"].update(load_knowledge_base_from_json(json_events))
    knowledge_base["emergency_services"].update(load_emergency_services_from_csv(csv_emergency))

    return knowledge_base
```

---

### **Using the Knowledge Base with the AI Model**

The key to this approach is making sure that if the knowledge base does not directly answer a user query, we **augment the prompt** sent to the AI model with relevant context from the knowledge base. This allows the model to generate more accurate responses, enriched by the localized data.

Here’s how you can update the `handle_user_input` function to ensure the knowledge base data is parsed through the model:

```python
def handle_user_input(flow, knowledge_base):
    """Handle user input, search the knowledge base, and augment the AI model's response with relevant data."""
    if prompt := st.chat_input("What is up?"):
        # Moderate input for profanity
        cleaned_prompt, is_profane = moderate_user_input(prompt)

        # Add the cleaned or original input to the session state
        st.session_state.messages.append({"role": "user", "content": cleaned_prompt})
        st.session_state.chat_history.append({"role": "user", "content": cleaned_prompt})

        # Show the original or censored input
        with st.chat_message("user"):
            st.markdown(cleaned_prompt)

        if is_profane:
            st.warning("Your input contained inappropriate language and has been censored.")

        # Search the knowledge base for a response
        response = search_knowledge_base(knowledge_base, cleaned_prompt)

        if not response:
            # If no response from the knowledge base, augment the OpenAI API request with knowledge base context
            utilities_context = " ".join([f"{k}: {v}" for k, v in knowledge_base["utilities"].items()])
            government_context = " ".join([f"{k}: {v}" for k, v in knowledge_base["government_services"].items()])
            transport_context = " ".join([f"{k}: {v['provider']}, {v['contact']}" for k, v in knowledge_base["transportation"].items()])

            # Build the augmented prompt with knowledge base data
            final_prompt = f"Here is relevant information about transportation, utilities, and government services in Atlanta:\nTransportation:\n{transport_context}\nUtilities:\n{utilities_context}\nGovernment Services:\n{government_context}\nUser question: {cleaned_prompt}"

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
```

---

### **Key Features**:
1. **Search Knowledge Base First**: Always check if the knowledge base has a direct answer.
2. **Augment AI Model Input**: If no direct answer is found, use the knowledge base data to add context to the AI model prompt.
3. **Unified Data Handling**: Load data from **TXT**, **CSV**, and **JSON** formats, ensuring all data points are available for the assistant.

---

### **Next Steps**

1. **Test the Knowledge Base**: Ensure that each category (transportation, schools, healthcare, events, emergency services) is loaded correctly.
2. **Optimize Performance**: Ensure the assistant can parse through the knowledge base efficiently while generating accurate, contextually relevant responses.
3. **Continue Expanding**: Keep adding data points and improving the knowledge base to make the assistant as helpful as possible for Atlanta newcomers.

This approach ensures that the **ATLien Assistant** provides rich, accurate, and context-sensitive responses by leveraging both the structured knowledge base and the AI model's capabilities.