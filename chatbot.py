import streamlit as st
from crewai import Crew, Process
from agents import reactjs_agent, angular_agent, javascript_agent, vuejs_agent, fullstack_agent, datascience_agent
from tasks import reactjs_task, angular_task, javascript_task, vuejs_task, fullstack_task, datascience_task
import asyncio

# Dynamically load agents and tasks
AGENTS = {
    "ReactJS": reactjs_agent,
    "Angular": angular_agent,
    "JavaScript": javascript_agent,
    "Vue.js": vuejs_agent,
    "Full Stack": fullstack_agent,
    "Data Science": datascience_agent
}

TASKS = {
    "ReactJS": reactjs_task,
    "Angular": angular_task,
    "JavaScript": javascript_task,
    "Vue.js": vuejs_task,
    "Full Stack": fullstack_task,
    "Data Science": datascience_task
}

# Forming the interview preparation crew with sequential task execution
def create_interview_crew(selected_topic):
    return Crew(
        agents=[AGENTS[selected_topic]],
        tasks=[TASKS[selected_topic]],
        process=Process.sequential,
        memory=True,
        cache=True,
        max_rpm=100,
        share_crew=True
    )

# Async function to kick off the interview preparation process
async def prepare_interview_async(crew, topic):
    try:
        result = await asyncio.to_thread(crew.kickoff, inputs={'topic': topic})
        return result
    except Exception as e:
        return f"Error during preparation: {str(e)}"

# Function to display the chatbot interface
def chatBot():
    st.title("🎓 Interview Preparation Chatbot")

    st.sidebar.title("Select Interview Topic")
    selected_topic = st.sidebar.selectbox(
        "Choose a topic:",
        list(AGENTS.keys())
    )

    # Initialize session state for messages and selected topic
    if "messages" not in st.session_state or st.session_state.get("selected_topic") != selected_topic:
        st.session_state["messages"] = [
            {"role": "assistant", "content": f"Hi! I am your {selected_topic} interview preparation assistant. How can I help you?"}
        ]
        st.session_state["selected_topic"] = selected_topic

    # Display the chat messages
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg['content'])

    # Handle user input
    if prompt := st.chat_input(placeholder=f"Ask a question about {selected_topic}..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Prepare the interview using the selected topic's crew
        interview_crew = create_interview_crew(selected_topic)

        # Display a progress spinner while processing the response
        with st.spinner("Preparing response..."):
            response = asyncio.run(prepare_interview_async(interview_crew, selected_topic))

        # Append the assistant's response and display it
        st.session_state.messages.append({'role': 'assistant', "content": response})
        st.chat_message("assistant").write(response)

    # Limit the number of messages to avoid bloating session state
    MAX_MESSAGES = 20
    if len(st.session_state["messages"]) > MAX_MESSAGES:
        st.session_state["messages"] = st.session_state["messages"][-MAX_MESSAGES:]

# Run the chatbot when the page is loaded
if __name__ == "__main__":
    chatBot()
