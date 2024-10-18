import os
import streamlit as st
import json
import aiohttp
import asyncio
import time

# API endpoint for code generation
url = os.getenv("API_URL", "http://13.235.69.82:11434/api/generate")

headers = {'Content-Type': 'application/json'}

# Function to load session data
def load_session_data():
    """Load session state data from a JSON file, or initialize a new session state."""
    if os.path.exists("session_data.json"):
        try:
            with open("session_data.json", "r") as f:
                data = json.load(f)
                # Load session state from file
                st.session_state.chatbot_queries = data.get("chatbot_queries", 0)
                st.session_state.code_prompts = data.get("code_prompts", 0)
                st.session_state.total_chatbot_time = data.get("total_chatbot_time", 0.0)
                st.session_state.total_code_time = data.get("total_code_time", 0.0)
                st.session_state.response_times = data.get("response_times", [])
        except (json.JSONDecodeError, FileNotFoundError):
            st.error("Error loading session data: Invalid or missing JSON file.")
            # Initialize session state if the file is invalid
            st.session_state.chatbot_queries = 0
            st.session_state.code_prompts = 0
            st.session_state.total_chatbot_time = 0.0
            st.session_state.total_code_time = 0.0
            st.session_state.response_times = []
    else:
        # Initialize session state if the file does not exist
        st.session_state.chatbot_queries = 0
        st.session_state.code_prompts = 0
        st.session_state.total_chatbot_time = 0.0
        st.session_state.total_code_time = 0.0
        st.session_state.response_times = []

# Call the function when loading the Streamlit app
load_session_data()

# Asynchronous function to generate a response from the API
async def run_code_llama(language, prompt):
    # Initialize session state variables
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'response_times' not in st.session_state:
        st.session_state.response_times = []
    if 'total_code_time' not in st.session_state:
        st.session_state.total_code_time = 0
    if 'code_prompts' not in st.session_state:
        st.session_state.code_prompts = 0  # Track how many code prompts have been done

    # Add the new prompt to history
    st.session_state.history.append(prompt)
    if len(st.session_state.history) > 10:  # Limit history to the last 10 entries
        st.session_state.history.pop(0)
    
    final_prompt = f"Language: {language}\n" + "\n".join(st.session_state.history)

    data = {
        "model": "LinguaLogic",
        "prompt": final_prompt,
        "stream": False
    }

    retry_attempts = 5
    timeout_duration = 120  # Increase timeout to 2 minutes

    for attempt in range(retry_attempts):
        try:
            start_time = time.time()  # Initialize start time here

            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data, timeout=timeout_duration) as response:
                    response.raise_for_status()  # Raise error for non-2xx statuses
                    
                    response_data = await response.json()

                    end_time = time.time()  # End timer
                    response_time = round(end_time - start_time, 2)

                    # Update session state with timing data
                    st.session_state.response_times.append(response_time)
                    st.session_state.total_code_time += response_time
                    st.session_state.code_prompts += 1

                    save_session_data()

                    if 'response' in response_data:
                        return response_data['response']
                    else:
                        return "Error: Invalid API response format."

        except aiohttp.ClientTimeout:
            st.warning(f"Request timed out, retrying {attempt + 1}/{retry_attempts}...")
            await asyncio.sleep(5)  # Wait before retrying

        except aiohttp.ClientError as e:
            return f"API Error: {str(e)}"

    return "API Error: Request timed out after multiple attempts."

# Function to save session data
def save_session_data():
    """Save session state data to a JSON file for persistence."""
    try:
        data = {
            "chatbot_queries": st.session_state.get('chatbot_queries', 0),
            "code_prompts": st.session_state.get('code_prompts', 0),
            "total_chatbot_time": st.session_state.get('total_chatbot_time', 0.0),
            "total_code_time": st.session_state.get('total_code_time', 0.0),
            "response_times": st.session_state.get('response_times', [])
        }
        with open("session_data.json", "w") as f:
            json.dump(data, f)
    except Exception as e:
        st.error(f"Error saving session data: {e}")

# Streamlit interface for standalone testing
def code_generation_interface():
    st.title("Code Generation with CodeGuru API")

    # Text area for user to input a coding prompt
    prompt = st.text_area("Enter your coding prompt:", key="code_prompt")

    # Language selection
    language = st.selectbox("Select Programming Language", ["Python", "Java", "JavaScript", "C++", "Go", "Rust"])

    # Button to trigger code generation
    if st.button("Generate Code"):
        if not prompt or len(prompt.strip()) < 10:  # Minimum length check for prompt
            st.warning("Please enter a more detailed prompt (at least 10 characters).")
            return

        # Use asyncio.create_task to schedule the async function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(run_code_llama(language, prompt))

        # Display the generated code with syntax highlighting
        st.write(f"### Generated Code for {language}:")
        st.code(response, language=language.lower())  # Adjust the language dynamically

    # Button to clear the history (reset conversation)
    if st.button("Clear History"):
        # Clear session state history and reset timings
        st.session_state.history = []
        st.session_state.response_times = []
        st.session_state.total_code_time = 0
        st.success("Session history cleared!")  # Notify the user that history was cleared

# Launch the Streamlit interface if running this script directly
if __name__ == "__main__":
    code_generation_interface()
