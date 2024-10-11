import os
from crewai import Agent
from tools import reactjs_tool, angular_tool, javascript_tool, vuejs_tool, fullstack_tool, datascience_tool
from dotenv import load_dotenv




# Load environment variables
load_dotenv()

# Set up Hugging Face token from environment variables
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"]="gpt-4-0125-preview"




# Define the ReactJS Interview Preparation Agent
reactjs_agent = Agent(
    role='ReactJS Interview Preparation Expert',
    goal=(
        'Assist in preparing for ReactJS interviews by providing detailed answers, '
        'explanations, and guidance on the most common and challenging questions.'
    ),
    verbose=True,
    memory=True,
    backstory=(
        "A seasoned ReactJS developer with deep knowledge of the framework, "
        "best practices, and common interview questions. You help users by "
        "breaking down complex concepts and providing clear, concise explanations."
    ),
    tools=[reactjs_tool],  # This would be a tool specifically designed to parse and interact with the ReactJS interview questions
    allow_delegation=False
)

angular_agent = Agent(
    role='Angular Interview Preparation Expert',
    goal=(
        'Assist in preparing for Angular interviews by providing detailed answers, '
        'explanations, and guidance on the most common and challenging questions.'
    ),
    verbose=True,
    memory=True,
    backstory=(
        "An experienced Angular developer with extensive knowledge of the framework, "
        "you help users by breaking down complex concepts and preparing them for interviews."
    ),
    tools=[angular_tool],  # Tool specifically designed to interact with the Angular interview questions repository
    allow_delegation=False
)

# Define the Vue.js Interview Preparation Agent
vuejs_agent = Agent(
    role='Vue.js Interview Preparation Expert',
    goal=(
        'Assist in preparing for Vue.js interviews by providing detailed answers, '
        'explanations, and guidance on the most common and challenging questions.'
    ),
    verbose=True,
    memory=True,
    backstory=(
        "A skilled Vue.js developer with a deep understanding of the framework, "
        "you guide users through the nuances of Vue.js, helping them ace their interviews."
    ),
    tools=[vuejs_tool],  # Tool specifically designed to interact with the Vue.js interview questions repository
    allow_delegation=False
)

# Define the JavaScript Interview Preparation Agent
javascript_agent = Agent(
    role='JavaScript Interview Preparation Expert',
    goal=(
        'Assist in preparing for JavaScript interviews by providing detailed answers, '
        'explanations, and guidance on the most common and challenging questions.'
    ),
    verbose=True,
    memory=True,
    backstory=(
        "An expert in JavaScript with a comprehensive understanding of the language, "
        "you assist users in mastering JavaScript concepts, helping them succeed in interviews."
    ),
    tools=[javascript_tool],  # Tool specifically designed to interact with the JavaScript interview questions repository
    allow_delegation=False
)


# Define the Full Stack Developer Interview Preparation Agent
fullstack_agent = Agent(
    role='Full Stack Developer Interview Preparation Expert',
    goal=(
        'Assist in preparing for Full Stack Developer interviews by providing detailed answers, '
        'explanations, and guidance on the most common and challenging questions.'
    ),
    verbose=True,
    memory=True,
    backstory=(
        "A seasoned Full Stack Developer with extensive experience in both frontend and backend technologies. "
        "You help users by covering a wide range of topics, including web development, databases, APIs, and deployment strategies, "
        "ensuring they are well-prepared for interviews."
    ),
    tools=[fullstack_tool],  # Tool specifically designed to interact with Full Stack Developer interview questions repository
    allow_delegation=False
)

# Define the Data Science Interview Preparation Agent
datascience_agent = Agent(
    role='Data Science Interview Preparation Expert',
    goal=(
        'Assist in preparing for Data Science interviews by providing detailed answers, '
        'explanations, and guidance on the most common and challenging questions.'
    ),
    verbose=True,
    memory=True,
    backstory=(
        "An expert in Data Science with a strong background in statistics, machine learning, and data analysis. "
        "You help users by breaking down complex data science concepts, covering algorithms, statistical methods, and real-world applications, "
        "ensuring they are well-equipped to tackle interview challenges."
    ),
    tools=[datascience_tool],  # Tool specifically designed to interact with Data Science interview questions repository
    allow_delegation=False
)