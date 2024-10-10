import requests
import json

# API endpoint for code generation
url = "http://localhost:11434/api/generate"
headers = {'Content-Type': 'application/json'}
history = []

# Function to generate a response from the API
def run_code_llama(language, prompt):
    """
    This function sends a code prompt and language to the API and returns the generated response.
    :param language: The programming language (e.g., 'Python', 'Java')
    :param prompt: The code generation prompt provided by the user
    :return: The generated code response or an error message
    """
    # Maintain a history of prompts
    history.append(prompt)
    final_prompt = f"Language: {language}\n" + "\n".join(history)

    # Data payload for the API
    data = {
        "model": "LinguaLogic",  # API model name
        "prompt": final_prompt,
        "stream": False
    }

    try:
        # Make the API request
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an error for bad responses
        response_data = response.json()
        # Extract the generated response from the API response
        actual_response = response_data.get('response', 'No response found')
        return actual_response
    except requests.exceptions.RequestException as e:
        # Return the error message if something goes wrong
        return f"Error: {str(e)}"

# Optional: Streamlit interface for standalone testing
def code_generation_interface():
    import streamlit as st
    st.title("Code Generation with CodeGuru API")

    # Text area for user to input a coding prompt
    prompt = st.text_area("Enter your coding prompt:", key="code_prompt")

    # Language selection
    language = st.selectbox("Select Programming Language", ["Python", "Java", "JavaScript", "C++", "Go", "Rust"])

    # Button to trigger code generation
    if st.button("Generate Code"):
        if prompt:
            # Generate the response by calling the API
            response = run_code_llama(language, prompt)
            # Display the generated code in a code block with syntax highlighting
            st.write(f"### Generated Code for {language}:")
            st.code(response, language=language.lower())  # Adjust language dynamically
        else:
            st.warning("Please enter a prompt to generate code.")

    # Button to clear the history (reset conversation)
    if st.button("Clear History"):
        global history
        history = []  # Reset the history
        st.success("History cleared!")  # Notify the user that the history has been cleared

# Launch the Streamlit interface if running this script directly
if __name__ == "__main__":
    code_generation_interface()
