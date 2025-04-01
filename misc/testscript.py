import streamlit as st
import openai
from crewai import Agent, Task, Crew, Process
from langchain.memory import ConversationBufferMemory
import logging

# Configure logging for CrewAI traceability
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Azure OpenAI Configuration
openai.api_type = "azure"
openai.api_key = "<YOUR_AZURE_OPENAI_KEY>"
openai.api_base = "https://<YOUR_AZURE_ENDPOINT>.openai.azure.com/"
openai.api_version = "2023-05-15"

# Initialize LangChain Memory
memory = ConversationBufferMemory()

# Define CrewAI Agents
intent_recognition_agent = Agent(
    name="Intent Recognizer",
    role="Identifies the intent behind the user's query.",
    tools=[],  # No tools needed here
    model="gpt-4",
    verbose=True
)

knowledge_retrieval_agent = Agent(
    name="Knowledge Retriever",
    role="Fetches relevant banking details based on the detected intent.",
    tools=[],  # You can integrate a knowledge base here
    model="gpt-4",
    verbose=True
)

upsell_agent = Agent(
    name="Upsell Recommender",
    role="Suggests relevant upsell or cross-sell opportunities.",
    tools=[],
    model="gpt-4",
    verbose=True
)

closure_agent = Agent(
    name="Closure Handler",
    role="Before the conversation ends, asks for a callback or promotional signup.",
    tools=[],
    model="gpt-4",
    verbose=True
)

# Define Tasks
intent_task = Task(
    description="Identify user's intent from the conversation.",
    agent=intent_recognition_agent
)

knowledge_task = Task(
    description="Retrieve relevant banking information based on user inquiry.",
    agent=knowledge_retrieval_agent
)

upsell_task = Task(
    description="Provide upsell or cross-sell options based on user's inquiry.",
    agent=upsell_agent
)

closure_task = Task(
    description="Ask user for callback preference and promotional email signup before ending.",
    agent=closure_agent
)

# Define Crew Workflow
banking_chatbot_crew = Crew(
    agents=[intent_recognition_agent, knowledge_retrieval_agent, upsell_agent, closure_agent],
    tasks=[intent_task, knowledge_task, upsell_task, closure_task],
    process=Process.sequential
)

def chat_with_bot(user_input):
    memory.save_context({"user": user_input}, {})
    result = banking_chatbot_crew.kickoff()
    memory.save_context({}, {"bot": result})
    return result

# Streamlit UI
st.title("Banking Chatbot with CrewAI and Azure OpenAI")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("You: ")
if st.button("Send") and user_input:
    response = chat_with_bot(user_input)
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Bot", response))

st.subheader("Chat History")
for sender, message in st.session_state.chat_history:
    st.write(f"**{sender}:** {message}")

