import streamlit as st
import requests
import json
import base64

# Constants for GitHub integration
GITHUB_USER = "hawkarabdulhaq"
GITHUB_REPO = "energyscan"
JSON_FILE = "data/awareness.json"
GITHUB_API_URL_JSON = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{JSON_FILE}"

def get_github_pat():
    """Retrieve GitHub PAT from Streamlit secrets."""
    try:
        return st.secrets["github_pat"]
    except KeyError:
        st.error("GitHub PAT not found in secrets! Please add `github_pat` to your secrets.")
        return None

def load_existing_data():
    """Load existing data from the GitHub repository."""
    github_pat = get_github_pat()
    if not github_pat:
        return []

    headers = {"Authorization": f"token {github_pat}"}
    response = requests.get(GITHUB_API_URL_JSON, headers=headers)

    if response.status_code == 200:
        content = response.json().get("content", "")
        if content:
            try:
                return json.loads(base64.b64decode(content).decode("utf-8"))
            except json.JSONDecodeError:
                st.error("Failed to decode existing data. Returning an empty list.")
                return []
    elif response.status_code == 404:
        st.warning("No existing data found.")
        return []
    else:
        st.error(f"Failed to fetch data from GitHub. Error {response.status_code}: {response.text}")
        return []

def analyze_responses(responses):
    """Analyze individual responses and identify areas for improvement."""
    insights = []
    if responses["q1"] == "No":
        insights.append("Understand your natural energy highs and lows during the day to enhance performance.")
    if responses["q2"] < 3:
        insights.append("Improve your ability to predict peak energy times by observing and journaling daily patterns.")
    if responses["q3"].startswith("D"):
        insights.append("Regularly track your energy levels to increase awareness.")
    if responses["q4"] < 3:
        insights.append("Consider scheduling demanding tasks during your peak energy hours for better productivity.")
    if "C. Push through regardless." in responses["q5"] or "D. Delay tasks until later." in responses["q5"]:
        insights.append("Adopt better strategies for low-energy periods, such as taking breaks or reprioritizing tasks.")
    if responses["q6"] == "No":
        insights.append("Maintain a consistent sleep schedule to enhance energy optimization.")
    if responses["q7"] < 3:
        insights.append("Schedule regular breaks during work hours to recharge and sustain productivity.")
    if responses["q8"] == "No":
        insights.append("Focus on techniques to feel more in control of your daily energy management.")
    if responses["q9"] < 3:
        insights.append("Work on improving your satisfaction with your energy management by refining routines.")
    return insights

def display_analysis():
    st.title("📊 Awareness Analysis")
    st.markdown("""
    **Identify Your Strengths and Areas for Improvement**  
    This section analyzes your responses to the Awareness Survey to provide actionable insights and recommendations.
    """)

    # Load data
    data = load_existing_data()
    if not data:
        st.warning("No data available for analysis.")
        return

    # Select a specific response to analyze
    st.markdown("### Select a Response to Analyze")
    selected_index = st.selectbox(
        "Choose a response:",
        options=list(range(len(data))),
        format_func=lambda i: f"Response {i + 1}"
    )
    selected_response = data[selected_index]["responses"]

    # Display analysis
    st.subheader("📋 Analysis Results")
    insights = analyze_responses(selected_response)
    if insights:
        st.markdown("**🔍 Areas for Improvement:**")
        for i, insight in enumerate(insights, 1):
            st.write(f"{i}. {insight}")
    else:
        st.success("🎉 Great job! No significant areas for improvement were identified.")

    # Display additional insights (e.g., scores)
    st.markdown("### 📊 Additional Insights")
    total_score = sum([
        4 if selected_response["q1"] == "Yes" else 2,
        selected_response["q2"],
        {"A": 4, "B": 3, "C": 2, "D": 1}[selected_response["q3"][0]],
        selected_response["q4"],
        sum({
            "A. Adjust tasks to match energy levels.": 4,
            "B. Take a short break or recharge.": 3,
            "C. Push through regardless.": 2,
            "D. Delay tasks until later.": 1
        }[strategy] for strategy in selected_response["q5"]),
        4 if selected_response["q6"] == "Yes" else 2,
        selected_response["q7"],
        4 if selected_response["q8"] == "Yes" else 2,
        selected_response["q9"]
    ])
    st.write(f"**Total Score:** {total_score}/40")

    # Display full response for context
    st.markdown("### 📄 Full Response Data")
    st.json(selected_response)
