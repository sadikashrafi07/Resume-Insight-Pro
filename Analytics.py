import streamlit as st
import plotly.express as px
import pandas as pd
import time
import json
import os

def analytics_page():
    # Custom CSS for professional styling and consistent layout
    st.markdown("""
        <style>
        .reportview-container {
            background-color: #202841;
            color: white;
        }
        .css-12oz5g7 {background-color: #202841;}
        .block-container {
            padding-top: 2rem;
        }
        h1, h2, h3, h4 {
            color: #d4d4dc;
            text-align: left;  /* Adjusted alignment */
        }
        .metric-container {
            background-color: #1f2e3d;
            border-radius: 10px;
            padding: 10px;
            text-align: left;  /* Ensure consistency */
            margin-bottom: 10px;
        }
        .metric-container div {
            color: #a8d1ff;
        }
        </style>
        """, unsafe_allow_html=True)

    # --- Data Persistence Functions ---
    def save_session_data():
        """Save session state data to a JSON file for persistence."""
        try:
            data = {
                "chatbot_queries": st.session_state.chatbot_queries,
                "code_prompts": st.session_state.code_prompts,
                "total_chatbot_time": st.session_state.total_chatbot_time,
                "total_code_time": st.session_state.total_code_time,
                "response_times": st.session_state.response_times
            }
            with open("session_data.json", "w") as f:
                json.dump(data, f)
            st.success("Session data saved successfully!")
        except Exception as e:
            st.error(f"Error saving session data: {e}")

    def load_session_data():
        """Load session state data from a JSON file if it exists."""
        try:
            if os.path.exists("session_data.json"):
                with open("session_data.json", "r") as f:
                    data = json.load(f)
                    st.session_state.chatbot_queries = data.get("chatbot_queries", 0)
                    st.session_state.code_prompts = data.get("code_prompts", 0)
                    st.session_state.total_chatbot_time = data.get("total_chatbot_time", 0.0)
                    st.session_state.total_code_time = data.get("total_code_time", 0.0)
                    st.session_state.response_times = data.get("response_times", [])
                    st.success("Session data loaded successfully!")
            else:
                # Initialize session state if no file exists
                st.session_state.chatbot_queries = 0
                st.session_state.code_prompts = 0
                st.session_state.response_times = []
                st.session_state.total_chatbot_time = 0.0
                st.session_state.total_code_time = 0.0
        except Exception as e:
            st.error(f"Error loading session data: {e}")

    # Load session data at the start
    load_session_data()

    # --- Dashboard Header ---
    st.markdown("<h1>📊 Professional Analytics Dashboard</h1>", unsafe_allow_html=True)

    # --- Data for Analytics ---
    if (st.session_state.chatbot_queries == 0 and 
        st.session_state.code_prompts == 0 and 
        st.session_state.total_chatbot_time == 0 and 
        st.session_state.total_code_time == 0):
        st.info("No data available for generating charts.")
        return  # Stop rendering further charts if no data exists

    data = {
        "Metrics": ["Chatbot Queries", "Code Prompts", "Chatbot Response Time (Total)", "Code Response Time (Total)"],
        "Values": [
            st.session_state.chatbot_queries, 
            st.session_state.code_prompts, 
            round(st.session_state.total_chatbot_time, 2), 
            round(st.session_state.total_code_time, 2)
        ]
    }

    df = pd.DataFrame(data)

    # --- Bar Chart: Chatbot Queries and Code Prompts ---
    st.markdown("<h2>Interaction Overview</h2>", unsafe_allow_html=True)
    bar_chart = px.bar(df, x="Metrics", y="Values", text="Values", title="Chatbot vs Code Prompts & Response Time",
                       color="Metrics", template="plotly_dark", height=400)
    bar_chart.update_layout(
        title_font_size=18,
        xaxis_title=None,
        yaxis_title=None,
        showlegend=False,
        margin=dict(l=40, r=40, t=50, b=40)
    )
    st.plotly_chart(bar_chart)

    # --- Pie Chart: Task Distribution ---
    st.markdown("<h2>Task Distribution</h2>", unsafe_allow_html=True)
    task_distribution_fig = px.pie(
        values=[st.session_state.chatbot_queries, st.session_state.code_prompts], 
        names=["Chatbot Queries", "Code Prompts"],
        title="Task Distribution",
        color_discrete_sequence=px.colors.sequential.Teal,
        hole=0.3
    )
    task_distribution_fig.update_traces(textinfo='percent+label', hoverinfo='label+percent+value')
    st.plotly_chart(task_distribution_fig)

    # --- Line Chart: Response Times ---
    st.markdown("<h2>Response Times Over Interactions</h2>", unsafe_allow_html=True)
    if st.session_state.response_times:
        response_times_df = pd.DataFrame({
            "Task": ["Chatbot" if i % 2 == 0 else "Code Generation" for i in range(len(st.session_state.response_times))],
            "Response Time (sec)": st.session_state.response_times
        })

        line_chart = px.line(response_times_df, x=response_times_df.index, y="Response Time (sec)", color="Task", 
                             title="Response Times Over Interactions", markers=True, template="plotly_dark", height=400)
        line_chart.update_layout(
            title_font_size=18,
            xaxis_title="Interaction Count",
            yaxis_title="Response Time (seconds)",
            legend_title_text="Task"
        )
        st.plotly_chart(line_chart)
    else:
        st.info("No response times recorded yet.")

    # --- Summary Section for Quick Stats ---
    st.markdown("<h2>Quick Stats</h2>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(label="Chatbot Queries", value=st.session_state.chatbot_queries)

    with col2:
        st.metric(label="Code Prompts", value=st.session_state.code_prompts)

    with col3:
        st.metric(label="Chatbot Total Time (s)", value=round(st.session_state.total_chatbot_time, 2))

    with col4:
        st.metric(label="Code Total Time (s)", value=round(st.session_state.total_code_time, 2))

    # Auto-save session data on button interaction
    if st.button("Save Session Data"):
        save_session_data()

    # Optional: Reset session data to default values
    if st.button("Reset Session Data"):
        default_data = {
            "chatbot_queries": 0,
            "code_prompts": 0,
            "total_chatbot_time": 0.0,
            "total_code_time": 0.0,
            "response_times": []
        }
        st.session_state.update(default_data)
        with open("session_data.json", "w") as f:
            json.dump(default_data, f)
        st.success("Session data reset successfully!")

    # Footer Section
    st.markdown("---")
    st.markdown("<p style='text-align: center;'>This professional analytics dashboard provides insights into chatbot queries, code generation prompts, and overall response times.</p>", unsafe_allow_html=True)
