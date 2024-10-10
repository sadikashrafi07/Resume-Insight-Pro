import os
import streamlit as st
import requests
import json
import time

# API endpoint for code generation
url = os.getenv("API_URL", "http://localhost:11434/api/generate")
headers = {'Content-Type': 'application/json'}

# Function to generate a response from the API with retry logic
def run_code_llama(language, prompt):
    # Initialize session state variables if needed
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

    # Prepare the data payload for the API
    data = {
        "model": "LinguaLogic",  # API model name
        "prompt": final_prompt,
        "stream": False
    }

    retry_attempts = 3  # Number of retries if the request times out
    timeout_duration = 30  # Increase timeout to 30 seconds

    for attempt in range(retry_attempts):
        try:
            start_time = time.time()  # Start timer

            # Make the request to the API with a timeout
            response = requests.post(url, headers=headers, data=json.dumps(data), timeout=timeout_duration)
            response.raise_for_status()  # Raise an exception for any non-200 status

            # Extract the response
            response_data = response.json()

            end_time = time.time()  # End timer
            response_time = round(end_time - start_time, 2)

            # Update session state with timing data
            st.session_state.response_times.append(response_time)
            st.session_state.total_code_time += response_time
            st.session_state.code_prompts += 1  # Update code prompts count

            # Save updated session state to file
            save_session_data()

            # Return the generated code from the API response
            if 'response' in response_data:
                return response_data['response']
            else:
                return "Error: Invalid API response format."

        except requests.exceptions.Timeout:
            st.warning(f"Request timed out, retrying {attempt + 1}/{retry_attempts}...")
            time.sleep(5)  # Wait for 5 seconds before retrying

        except requests.exceptions.RequestException as e:
            # Return a detailed error message for any request failure
            return f"API Error: {str(e)}"

    # If all attempts fail
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

# Optional: Streamlit interface for standalone testing
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
        
        # Generate the response by calling the API
        response = run_code_llama(language, prompt)

        # Display the generated code with syntax highlighting
        st.write(f"### Generated Code for {language}:")
        st.code(response, language=language.lower())  # Adjust the language dynamically

    # Button to clear the history (reset conversation)
    if st.button("Clear History"):
        # Clear session state history and reset timings
        st.session_state.history = []
        st.session_state.response_times = []
        st.session_state.total_code_time = 0
        st.success("History cleared!")  # Notify the user that history was cleared

# Launch the Streamlit interface if running this script directly
if __name__ == "__main__":
    code_generation_interface()
