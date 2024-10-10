import streamlit as st
from crewai import Crew, Process
import asyncio
from programming import run_code_llama  # Import programming model logic

# Dynamically load agents and tasks
AGENTS = {
    "ReactJS": "reactjs_agent",
    "Angular": "angular_agent",
    "JavaScript": "javascript_agent",
    "Vue.js": "vuejs_agent",
    "Full Stack": "fullstack_agent",
    "Data Science": "datascience_agent"
}

TASKS = {
    "ReactJS": "reactjs_task",
    "Angular": "angular_task",
    "JavaScript": "javascript_task",
    "Vue.js": "vuejs_task",
    "Full Stack": "fullstack_task",
    "Data Science": "datascience_task"
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

# Function to handle programming logic
def handle_programming_task(language, prompt):
    return run_code_llama(language, prompt)

# Function to display the chatbot interface
def chatBot():
    st.title("🎓 Interview Preparation Chatbot")

    # Info message
    info_message = "ℹ️ Please select a category to proceed: Interview Preparation or Programming."

    # Create a background "bar" container to hold the dropdowns
    with st.container():
        st.markdown("""
            <style>
                .category-bar {
                    background-color: #333;
                    padding: 10px;
                    border-radius: 8px;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                }
                .category-bar select, .category-bar .stTextInput {
                    background-color: #262730;
                    color: white;
                }
            </style>
        """, unsafe_allow_html=True)

        # Dropdown bar to select categories and dynamically expand
        with st.container():
            col1, col2 = st.columns([2, 3], gap="medium")  # Two columns for dropdowns

            # First dropdown to select category
            with col1:
                category = st.selectbox("Choose Category", ["Select Type", "Interview Preparation", "Programming"], key="category_type", index=0)

            # Second dropdown dynamically updates based on selected category
            with col2:
                if category == "Interview Preparation":
                    selected_topic = st.selectbox("Choose Interview Topic:", list(AGENTS.keys()), key="interview_topic")
                elif category == "Programming":
                    language = st.selectbox("Select Programming Language", ["Python", "Java", "JavaScript", "C++", "Go", "Rust"], key="programming_language")

    # Show an info message below if "Select Type" is selected
    if category == "Select Type":
        st.info(info_message)
        st.stop()  # Prevent the rest of the UI from rendering until a valid category is chosen

    # Display logic for Interview Preparation
    if category == "Interview Preparation":
        # Prepare chat interface for Interview Preparation
        if "messages" not in st.session_state or st.session_state.get("selected_topic") != selected_topic:
            st.session_state["messages"] = [
                {"role": "assistant", "content": f"Hi! I am your {selected_topic} interview preparation assistant. How can I help you?"}
            ]
            st.session_state["selected_topic"] = selected_topic

        # Display the chat messages
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg['content'])

        # Handle user input for interview preparation
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

        # **Show Clear Chat History button in the sidebar** only after messages appear
        if "messages" in st.session_state and len(st.session_state["messages"]) > 1:  # Ensure there's user interaction
            st.sidebar.button("Clear Chat History", on_click=lambda: st.session_state.update({"messages": [], "selected_topic": None}))

    # Display logic for Programming
    elif category == "Programming":
        # Input for programming task (coding prompt)
        prompt = st.text_area("Enter your coding prompt:", key="code_prompt")

        # Generate Code Button
        if st.button("Generate Code"):
            if prompt:
                # Generate code using Code Llama logic from programming.py
                response = handle_programming_task(language, prompt)
                st.write(f"**Generated Code for {language}:**")
                st.code(response, language=language.lower())  # Display the generated code with formatting

                # After output, show the Clear Chat History button below the output
                st.markdown("<br>", unsafe_allow_html=True)  # Add space after the output
                if st.button("Clear Chat History"):
                    st.session_state["messages"] = []  # Clear the message history
            else:
                st.warning("Please enter a prompt to generate code.")

    # Limit the number of messages to avoid bloating session state
    MAX_MESSAGES = 20
    if len(st.session_state.get("messages", [])) > MAX_MESSAGES:
        st.session_state["messages"] = st.session_state["messages"][-MAX_MESSAGES:]

# Run the chatbot when the page is loaded
if __name__ == "__main__":
    # Initialize session state for messages if not already initialized
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    chatBot()
