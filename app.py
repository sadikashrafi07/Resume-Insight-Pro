import streamlit as st
from chatbot import chatBot
from streamlit_option_menu import option_menu
from dotenv import load_dotenv
import base64
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai
import time
import asyncio
import logging

# Streamlit App configuration
st.set_page_config(page_title="ATS Resume Expert", layout="wide")

# Initialize session state
if 'submit_contact_form' not in st.session_state:
    st.session_state.submit_contact_form = False

if 'response' not in st.session_state:
    st.session_state.response = None

if 'message' not in st.session_state:
    st.session_state.message = None

if 'message_time' not in st.session_state:
    st.session_state.message_time = None

if 'search_query' not in st.session_state:
    st.session_state.search_query = ""

if 'search_history' not in st.session_state:
    st.session_state.search_history = []

if 'resume_count' not in st.session_state:
    st.session_state.resume_count = 0

if 'total_analysis_time' not in st.session_state:
    st.session_state.total_analysis_time = 0

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Utility Functions

def load_profile_image(image_path):
    """Load a profile image and return it as a base64 encoded string."""
    try:
        with open(image_path, "rb") as file:
            data = file.read()
            return base64.b64encode(data).decode("utf-8")
    except FileNotFoundError:
        st.error(f"Image file not found at path: {image_path}")
        return None

def load_assets():
    """Load external CSS and JavaScript files."""
    try:
        with open("Assets/style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError as e:
        st.error(f"File not found: {e}")

def load_external_css(file_name):
    """Load additional CSS file."""
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file not found: {file_name}")

def input_pdf_setup(uploaded_file):
    """Convert an uploaded PDF file to an image format for processing."""
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

async def get_gemini_response_async(input_text, pdf_content, prompt):
    """Get a response from the Google Gemini AI model asynchronously."""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = await asyncio.to_thread(model.generate_content, [input_text, pdf_content[0], prompt])
        return response.candidates[0].content.parts[0].text
    except (KeyError, IndexError, AttributeError) as e:
        st.error(f"Error generating response: {e}")
        return "No text generated"

def handle_submission(uploaded_file, input_text, input_prompt):
    """Handle the submission process for analyzing resumes asynchronously."""
    if uploaded_file is not None:
        try:
            pdf_content = input_pdf_setup(uploaded_file)
            progress_bar = st.progress(0)
            analysis_time_start = time.time()

            response = asyncio.run(get_gemini_response_async(input_text, pdf_content, input_prompt))

            st.session_state.response = response  # Store the response in session state
            st.session_state.message = ('success', "Resume analyzed successfully!")
            st.session_state.message_time = time.time()

            # Update progress bar
            progress_bar.progress(100)

            # Track total time spent and resume count
            analysis_time_end = time.time()
            st.session_state.total_analysis_time += (analysis_time_end - analysis_time_start)
            st.session_state.resume_count += 1

        except Exception as e:
            st.session_state.response = None
            st.session_state.message = ('error', f"An error occurred: {e}")
            st.session_state.message_time = time.time()
    else:
        st.session_state.response = None
        st.session_state.message = ('warning', "Please upload the resume")
        st.session_state.message_time = time.time()

def create_button_grid(layout, uploaded_file, input_text):
    """Dynamically create a grid of buttons based on the provided layout."""
    for row_layout in layout:
        cols = st.columns(len(row_layout))
        for col, label in zip(cols, row_layout):
            with col:
                if st.button(label):
                    handle_submission(uploaded_file, input_text, label)

def export_result_as_text():
    """Allow the user to export the analysis result as a text file."""
    if st.session_state.response:
        result_text = st.session_state.response
        st.download_button(
            label="Download Analysis as Text",
            data=result_text.encode(),
            file_name="resume_analysis.txt",
            mime="text/plain"
        )

# Load assets and profile image
load_assets()
profile_image = load_profile_image("Images/profile.jpg")

# Sidebar Configuration
with st.sidebar:
    if profile_image:
        image_html = f'<div class="sidebar-image-container"><img src="data:image/jpeg;base64,{profile_image}" class="sidebar-image" alt="Profile Picture"></div>'
        st.markdown(image_html, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="sidebar-header">
            <h4 class="first-line">Hello, It's Me</h4>
            <h3 class="second-line">Angadi Mohammad Sadiq</h3>
            <h4 class="third-line">And I'm a <span class="typed-text">Software Developer!</span></h4>
        </div>
        <div class="social-media">
            <a href="http://linkedin.com/in/angadi-mohammad-sadiq" target="_blank"><i class='bx bxl-linkedin-square'></i></a>
            <a href="http://github.com/sadikashrafi07"><i class='bx bxl-github'></i></a>
            <a href="https://www.instagram.com/sadik.ashrafi?igsh=MXg5Y3lrb3hxMjUzdw=="><i class='bx bxl-instagram-alt'></i></a>
            <a href="https://twitter.com/sadikashrafi_01"><i class='bx bxl-twitter'></i></a>
        </div>                    
    """, unsafe_allow_html=True)

    # Load Boxicons CSS
    st.markdown(
        '<link href="https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css" rel="stylesheet">',
        unsafe_allow_html=True
    )

    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "chatBot", "Analytics", "Contact"],
        icons=["house", "robot", "bar-chart", "envelope"],
        menu_icon="cast",
        default_index=0,
        key="main_menu"
    )

# Main Page Rendering
if selected == "Home":
    st.markdown('<a name="home"></a>', unsafe_allow_html=True)

    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    # Typed.js integration for the typing animation on the Home page
    typing_animation = """
    <style>
        .center-typed {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100px;
            margin-top: 20px;
        }
        .typed-text {
            font-size: 2.5rem;
            font-weight: 400;
            color: #0ef;
            text-align: center;
        }
    </style>

    <div class="center-typed">
        <span id="typed-text" class="typed-text"></span>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/typed.js@2.0.11"></script>
    <script>
    document.addEventListener("DOMContentLoaded", function() {
        new Typed('#typed-text', {
            strings: ['ATS Tracking System'],
            typeSpeed: 100,
            backSpeed: 100,
            backDelay: 1000,
            loop: true
        });
    });
    </script>
    """
    st.components.v1.html(typing_animation, height=150)

    load_external_css(os.path.join('Assets', 'style.css'))  # Load the separate new features CSS file

    # Reduced space between Typed.js animation and Select Role
    st.markdown("<div style='margin-top: -20px;'></div>", unsafe_allow_html=True)

    # User role selection
    user_type = st.selectbox("Select your role", ["Select Role", "Recruiter", "Job Seeker"])
    input_text = st.text_area("Job Description: ", key="job_description")
    uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

    if uploaded_file is not None:
        st.session_state.message = ('success', "PDF Uploaded Successfully")
        st.session_state.message_time = time.time()

    # Prompts Definitions for Recruiters and Job Seekers
    recruiter_prompts = [
        "Skill Gap Analysis", 
        "Candidate Ranking", 
        "Cultural Fit Evaluation", 
        "Diversity and Inclusion Metrics", 
        "Keyword Frequency Analysis", 
        "Red Flag Detection"
    ]

    job_seeker_prompts = [
        "Tell Me About the Resume", 
        "Missing Keywords", 
        "Percentage Match", 
        "Actionable Feedback for Improvement", 
        "Role Fit Suggestions", 
        "Career Growth Potential", 
        "Resume Tailoring Suggestions", 
        "Cover Letter Generation", 
        "Job Fit Score", 
        "Resume Length Optimization", 
        "Achievement-Based Suggestions"
    ]

    # Create a placeholder for messages
    message_placeholder = st.empty()

    # Display prompts based on selected user type
    if user_type == "Recruiter":
        st.subheader("Recruiter Prompts")
        layout = [
            recruiter_prompts[:3], 
            recruiter_prompts[3:]
        ]
        create_button_grid(layout, uploaded_file, input_text)

    elif user_type == "Job Seeker":
        st.subheader("Job Seeker Prompts")
        
        # Custom layout based on your requirements
        layout = [
            ["Tell Me About the Resume", "Percentage Match", "Missing Keywords", "Role Fit Suggestions"],
            ["Actionable Feedback for Improvement", "Achievement-Based Suggestions", "Resume Tailoring Suggestions"],
            ["Resume Length Optimization", "Job Fit Score", "Cover Letter Generation", "Career Growth Potential"]
        ]
        create_button_grid(layout, uploaded_file, input_text)

    else:
        st.info("Please select Role to view the Suggestions.")

    # Display the response after all buttons
    if st.session_state.response:
        st.subheader("The Response is")
        st.write(st.session_state.response)
        
        # Provide option to download the response as a text file
        export_result_as_text()

    # Display the message if available and clear it after 3 seconds
    if st.session_state.message:
        message_type, message_text = st.session_state.message
        current_time = time.time()

        if message_type == 'success':
            message_placeholder.success(message_text)
        elif message_type == 'warning':
            message_placeholder.warning(message_text)
        elif message_type == 'error':
            message_placeholder.error(message_text)

        # Check if 3 seconds have passed since the message was set
        if current_time - st.session_state.message_time > 3:
            message_placeholder.empty()
            st.session_state.message = None

# Analytics Page
elif selected == "Analytics":
    st.title("Analytics Dashboard")
    st.markdown(f"**Resumes Analyzed**: {st.session_state.resume_count}")
    st.markdown(f"**Total Time Spent**: {round(st.session_state.total_analysis_time, 2)} seconds")
    st.markdown("This section shows how many resumes you’ve analyzed and how much time has been spent on the analysis.")

# chatBot Page
elif selected == "chatBot":
    chatBot()

# Contact Page
elif selected == "Contact":
    if st.session_state.get("form_submitted", False):
        st.success("Thank you! Your message has been sent.")
    else:
        st.markdown("""
        <section class="contact" id="contact">
            <h2 class="heading">Contact <span>Me!</span></h2>
            <form action="https://api.web3forms.com/submit" method="POST">
                <div class="input-box">
                    <input type="hidden" name="access_key" value="5c2d90d6-d1f2-4b74-b71e-1ce3865cc603">
                    <input type="hidden" name="_captcha" value="False">
                    <input type="text" name="name" class="item" placeholder="Full Name" required>
                    <input type="email" name="email" class="item" placeholder="Email Address" required>
                </div>
                <div class="input-box">
                    <input type="text" name="phone" id="phone" class="item" placeholder="Mobile Number" pattern="\\d{10}" title="Please enter valid Phone number" required>
                    <input type="text" name="subject" class="item" placeholder="Email Subject" required>
                </div>
                <textarea name="message" class="item textarea-field" cols="30" rows="5" placeholder="Your Message" required></textarea>
                <button type="submit" class="btn">Send Message</button>
            </form>
        </section>

        <footer class="footer">
            <div class="footer-text">
                <p>&copy; 2023 by AMS | All Rights Reserved.</p>
                <div class="footer-iconTop">
                    <a href="/" title="Go to Home"><i class='bx bx-left-arrow-alt'></i></a>
                </div>
            </div>
        </footer>
        """, unsafe_allow_html=True)

        # JavaScript validation for phone number
        st.markdown("""
        <script>
            document.addEventListener("DOMContentLoaded", () => {
                const phone = document.getElementById('phone');
                const form = document.querySelector('form');
                
                form.addEventListener("submit", (e) => {
                    if (!phone.value.match(/^\\d{10}$/)) {
                        e.preventDefault();
                        alert("Please enter exactly 10 digits for the phone number.");
                        phone.classList.add("error");
                    }
                });

                phone.addEventListener("keyup", () => {
                    if (phone.value.match(/^\\d{10}$/)) {
                        phone.classList.remove("error");
                    }
                });
            });
        </script>
        """, unsafe_allow_html=True)

# Server-side code to handle the form submission
query_params = st.query_params  # Access the query parameters directly
if query_params.get("form_submitted", ["false"])[0] == "true":
    st.session_state["form_submitted"] = True
    st.experimental_set_query_params(form_submitted="false")
