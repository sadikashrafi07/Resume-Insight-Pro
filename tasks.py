from crewai import Task
from tools import reactjs_tool, angular_tool, javascript_tool, vuejs_tool, fullstack_tool, datascience_tool
from agents import reactjs_agent, angular_agent, javascript_agent, vuejs_agent, fullstack_agent, datascience_agent

# ReactJS Interview Preparation Task
reactjs_task = Task(
    description=(
        "Prepare detailed answers and explanations for common ReactJS interview questions. "
        "Focus on breaking down complex concepts and providing clear guidance."
    ),
    expected_output='A comprehensive guide to ReactJS interview preparation, including explanations of common and challenging questions.',
    tools=[reactjs_tool],
    agent=reactjs_agent,
)

# Angular Interview Preparation Task
angular_task = Task(
    description=(
        "Prepare detailed answers and explanations for common Angular interview questions. "
        "Focus on complex concepts and ensure clarity in the explanations."
    ),
    expected_output='A thorough guide to Angular interview preparation, covering both basic and advanced questions.',
    tools=[angular_tool],
    agent=angular_agent,
)

# Vue.js Interview Preparation Task
vuejs_task = Task(
    description=(
        "Prepare detailed answers and explanations for common Vue.js interview questions. "
        "Highlight key concepts and provide clear guidance for interview preparation."
    ),
    expected_output='A detailed Vue.js interview preparation guide, focusing on key concepts and challenging questions.',
    tools=[vuejs_tool],
    agent=vuejs_agent,
)

# JavaScript Interview Preparation Task
javascript_task = Task(
    description=(
        "Prepare detailed answers and explanations for common JavaScript interview questions. "
        "Cover fundamental concepts as well as advanced topics relevant to interviews."
    ),
    expected_output='An in-depth JavaScript interview preparation guide, covering essential topics and challenging questions.',
    tools=[javascript_tool],
    agent=javascript_agent,
)

# Full Stack Developer Interview Preparation Task
fullstack_task = Task(
    description=(
        "Prepare comprehensive answers and explanations for Full Stack Developer interview questions. "
        "Cover both frontend and backend topics, including web development, databases, APIs, and deployment strategies."
    ),
    expected_output='A complete Full Stack Developer interview preparation guide, including both frontend and backend questions.',
    tools=[fullstack_tool],
    agent=fullstack_agent,
)

# Data Science Interview Preparation Task
datascience_task = Task(
    description=(
        "Prepare detailed answers and explanations for Data Science interview questions. "
        "Focus on algorithms, statistical methods, machine learning, and real-world applications."
    ),
    expected_output='An exhaustive Data Science interview preparation guide, covering algorithms, statistics, and machine learning.',
    tools=[datascience_tool],
    agent=datascience_agent,
)
