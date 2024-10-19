
# Resume Insight Pro

**Live Link**: [Resume Insight Pro](https://resume-insight-pro.streamlit.app/)

## Overview

**Resume Insight Pro** is a comprehensive tool designed for **job seekers** and **recruiters** to analyze and optimize resumes against job descriptions. It provides keyword suggestions, detailed feedback, and a search feature to query specific terms within resumes and job descriptions. The tool offers interactive support for interview preparation topics and coding problems.

It leverages multiple AI models and services:
- **CrewAI Multi-Agent system** and **GPT-4-0125-preview** for interview topic assistance.
- **LinguaLogic**, a custom model built on **CodeLlama**, for real-time code generation.
- **Amazon AWS EC2** to host the LinguaLogic model, handling heavy computational tasks.

The project also features a **real-time analytics dashboard** to track and visualize user interactions such as queries, code prompts, and response times, providing valuable insights into user behavior.

## Features

- **Resume Analysis**: Upload resumes (PDF) and get optimized suggestions based on job descriptions.
- **Keyword Suggestions**: Automatically suggest keywords to improve resume alignment with job descriptions.
- **Interview Preparation**: Offers support for technical interview topics (e.g., ReactJS, Data Science).
- **Code Generation**: Solve programming problems with code suggestions using the LinguaLogic model.
- **Real-Time Analytics**: Visualize user interactions, including total queries and response times.
- **Web3 Forms Integration**: Collects user feedback and suggestions for continuous improvement.

## Objectives

The main objectives of **Resume Insight Pro** are:
- To help job seekers improve their resumes to better match job descriptions.
- To provide recruiters with tools for quickly assessing resume quality.
- To offer interactive support for interview preparation and coding challenges.
- To track user behavior through real-time analytics for further improvements.

## Problem Statement

Job seekers and recruiters often face challenges in ensuring that resumes are aligned with job descriptions. Additionally, technical interview preparation and solving coding problems can be time-consuming. **Resume Insight Pro** addresses these issues by providing:
- Automated resume analysis and keyword suggestions.
- Interview preparation tools using advanced AI.
- Code generation for programming tasks, simplifying problem-solving.

## Tech Stack

- **Front-End**: Streamlit
- **Back-End**: Python, Streamlit, CrewAI
- **AI Models**: GPT-4-0125-preview, LinguaLogic (built on CodeLlama)
- **Cloud Services**: Amazon AWS EC2 (for LinguaLogic model)
- **APIs**: Google API, Web3Forms API
- **Analytics**: Plotly for real-time dashboard visualizations
- **Containerization**: Docker

## Setup Instructions

### Prerequisites

- **Python 3.10+**
- **Streamlit**
- **Docker** (for running the app in a container)
- **AWS EC2** (for hosting the LinguaLogic model, if running the model locally is required)

### Local Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repository/resume-insight-pro.git
   cd resume-insight-pro
   ```

2. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Create a `.env` file in the root directory and add your API keys:
     ```
     OPENAI_API_KEY=your-openai-api-key
     GOOGLE_API_KEY=your-google-api-key
     WEB3FORMS_ACCESS_KEY=your-web3forms-api-key
     API_URL=your-aws-ec2-endpoint
     ```

4. **Run the app**:
   ```bash
   streamlit run app.py
   ```

5. **Access the application**:
   - The app will be available at `http://localhost:8501`.

### Running with Docker

1. **Pull the Docker image**:
   ```bash
   docker pull sadiq07/resume-insight-pro
   ```

2. **Run the Docker container**:
   ```bash
   docker run -p 8501:8501 --env-file .env sadiq07/resume-insight-pro
   ```

3. **Access the application**:
   - Visit `http://localhost:8501` in your browser.

> **Note**: Ensure that your `.env` file is in the same directory where you run the `docker run` command. This file should contain the necessary environment variables for your application to function correctly.

## AWS EC2 Integration for LinguaLogic Model

To enable real-time code generation using the **LinguaLogic** model:
1. Set up an **AWS EC2** instance (e.g., `r5.xlarge`) and load the LinguaLogic model built on **CodeLlama**.
2. Make sure the model is accessible via the **API_URL** environment variable.
3. The Streamlit app will call this endpoint to generate code solutions.

For more details on setting up the model and endpoints, refer to [Ollama API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md).

## Usage

1. **Resume Analysis**:
   - Upload a PDF resume and provide a job description to receive keyword suggestions and actionable feedback for improvement.

2. **Interview Preparation**:
   - Choose a topic like ReactJS, Data Science, etc., and interact with the CrewAI multi-agent system to simulate interview scenarios.

3. **Code Generation**:
   - Input a programming prompt, and the app will generate code solutions using the **LinguaLogic** model.

4. **Real-Time Analytics**:
   - Monitor user interactions, including query count, code prompts, and response times, through the analytics dashboard.
  
## Feature Enhancements

### Planned Features

- **Search Bar with Query Support (RAG Application)**:  
  The **Home page** currently provides useful suggestions for users. In the next enhancement, a **search bar** will be added, allowing users to input custom queries. This feature will leverage a **Retrieval-Augmented Generation (RAG)** system, maintaining conversation history and session state for a more dynamic, personalized experience.

- **Interview Preparation Improvements**:  
  The **Interview Preparation** section will soon feature a curated list of **useful questions** and **most-asked questions** across different technical domains. Additionally, learning resources and further suggestions will be included to make this section a more comprehensive preparation tool for users. Users will also be able to **prepare their own professional resumes** based on feedback and suggestions provided by the platform, helping them achieve their dream jobs. Furthermore, users can submit their resumes for **professional review** by industry experts or working professionals to get additional insights.

- **Resume Optimization with AI**:  
  A future enhancement will allow the platform to provide **AI-powered resume templates** and **dynamic resume-building tools**. Users will be able to choose from various templates based on their career level and industry, and the system will recommend improvements as they build their resumes, ensuring that their resumes meet the latest industry standards.

- **Collaborative Resume Reviews**:  
  Integrating a **collaborative review system** where users can share their resumes with peers, mentors, or professionals for feedback. This feature would facilitate multiple rounds of feedback, helping users refine their resumes iteratively.

## Feedback

We value your feedback and suggestions. Please reach out to us at [angadimohammadsadiq@gmail.com](mailto:angadimohammadsadiq@gmail.com) for any inquiries or improvements you would like to suggest.

## Conclusion

**Resume Insight Pro** is an advanced tool that bridges the gap between job seekers and recruiters by offering insightful resume analysis and interview preparation tools. The integration of AI models such as **GPT-4-0125-preview** and **LinguaLogic** ensures robust and dynamic solutions for resume optimization and coding problems.

The real-time analytics dashboard further enhances user experience by providing actionable insights based on user interactions.
