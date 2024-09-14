# Practical AI Web Development with Streamlit, Promptflow, and PHI-3

## Welcome to the Practical AI Web Development Workshop, where we’ll guide you step-by-step through building a real-world AI-powered web application. Today’s session focuses on not just theory but hands-on application — you’ll leave this workshop with a fully functional AI solution that can be deployed in a real-world scenario.

---

## Purpose of the Workshop

In spite of the increasing demand for AI knowledge, many of the people giving talks and courses on the subject have never been in the room when an actual AI application was being built or deployed. This disconnect is diluting the knowledge base of the AI community, leading to a gap between theory and real-world application.

In this workshop, we’re doing things differently. The focus is on giving you hands-on experience with the thought processes behind building a real AI application. You won’t just be learning concepts — you’ll be immersed in the practical steps that go into developing an AI-powered solution. From problem-solving, decision-making, to handling real-world challenges, you’ll walk away with a genuine understanding of what it takes to bring an AI application to life.

---

## What We Are Building

### 🍑 ATLien Assistant

**Problem Statement**  
Moving to a new city is challenging. Whether it’s finding the right neighborhood, understanding local services, or navigating transportation, newcomers often face a steep learning curve. Traditional resources like websites or forums provide fragmented information, and it can be difficult to get personalized, relevant answers quickly.

The **ATLien Assistant** is an AI-powered virtual guide designed to help newcomers and residents of Atlanta navigate the city with ease. Instead of spending hours searching across various platforms, users can simply ask the assistant questions about neighborhoods, landmarks, transportation options, local hotspots, public services, upcoming events, and more. **ATLien Assistant** provides personalized, contextually relevant insights in a conversational format, delivering immediate answers tailored to individual needs.

With deep knowledge of Atlanta’s culture, lifestyle, and opportunities, the assistant serves as a comprehensive resource. Whether you’re looking for the best neighborhoods, local restaurants, or transportation advice, **ATLien Assistant** streamlines the process of finding useful information — all at your fingertips.

---

## What You Will Learn

In this workshop, you’ll learn how to build an AI-powered web app that not only works well but also reflects ethical standards, a clear brand voice, and high performance. By the end, you’ll be ready to deploy an AI solution that’s practical and thoughtful. Here’s what we’ll cover:

1. **Building Responsible AI (RAI)**
   - We’ll explore the importance of Responsible AI, focusing on how to ensure your app provides accurate, fair, and unbiased information. You’ll learn strategies to prevent misinformation, handle sensitive topics, and make your AI transparent to users.

2. **Defining Your Brand Voice**
   - Your AI assistant needs to sound consistent and reflect the personality of the brand or application. We’ll work on crafting a clear, recognizable Brand Voice that mirrors the values and tone of the assistant’s purpose. The goal is to ensure that the assistant always communicates in a way that aligns with your app’s mission and personality.

3. **Building Your Knowledge Base**
   - Your AI assistant can only be as accurate as the data it draws from. We’ll dive into building a robust knowledge base that pulls from a variety of file formats and APIs to ensure the AI is well-informed. We’ll also explore how to augment the AI model’s output with specific, relevant data from this knowledge base, particularly when users ask about local services or specific details.

4. **Managing Latency and Performance**
   - Performance is key. We’ll cover techniques to reduce latency so your AI assistant responds quickly, keeping the user experience smooth. You’ll learn how to optimize API usage, minimize delays, and handle user queries efficiently, even under heavy loads.

5. **Using a Multi-Model Approach for Better Results**
   - We’ll demonstrate how to implement a multi-model approach using **PHI-3** (a Small Language Model) and other models like **GPT-3.5** to handle different tasks more effectively. This approach leverages PHI-3 for structured queries and specialized tasks, while reserving larger models for more complex, open-ended queries, optimizing performance and cost efficiency.

---

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://chatbot-template.streamlit.app/)

## A simple Streamlit app that shows how to build a chatbot using **PHI-3**.

---

### How to run it on your own machine

1. Install the requirements:

   ```bash
   $ pip install -r requirements.txt
   ```

2. Run the app:

   ```bash
   $ streamlit run streamlit_app.py
   ```

---

### Features

- AI-powered virtual assistant for Atlanta
- Real-time personalized insights about neighborhoods, restaurants, and local events
- Uses **PHI-3** for both conversational responses and structured data queries
- Integrated APIs for real-time data such as traffic updates and events

---

Explore Atlanta with the power of AI!
