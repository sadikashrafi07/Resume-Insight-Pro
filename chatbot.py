import streamlit as st
from crewai import Crew, Process
from agents import reactjs_agent, angular_agent, javascript_agent, vuejs_agent, fullstack_agent, datascience_agent
from tasks import reactjs_task, angular_task, javascript_task, vuejs_task, fullstack_task, datascience_task

# Forming the interview preparation crew with sequential task execution
interview_crew = Crew(
    agents=[reactjs_agent, angular_agent, javascript_agent, vuejs_agent, fullstack_agent, datascience_agent],
    tasks=[reactjs_task, angular_task, javascript_task, vuejs_task, fullstack_task, datascience_task],
    process=Process.sequential,
    memory=True,
    cache=True,
    max_rpm=100,
    share_crew=True
)

# Function to kick off the interview preparation process based on a dynamic query
def prepare_interview(topic):
    result = interview_crew.kickoff(inputs={'topic': topic})
    return result

# Function to display the chatbot interface
def chatBot():
    st.title("🎓 Interview Preparation Chatbot")

    st.sidebar.title("Select Interview Topic")
    selected_topic = st.sidebar.selectbox(
        "Choose a topic:",
        ["ReactJS", "Angular", "JavaScript", "Vue.js", "Full Stack", "Data Science"]
    )

    # Initialize or update session state for messages
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

        # Run the agent based on the selected topic
        response = interview_crew.kickoff(inputs={'topic': selected_topic})
        
        st.session_state.messages.append({'role': 'assistant', "content": response})
        st.chat_message("assistant").write(response)