import streamlit as st
import requests
import json
import base64
import plotly.express as px

# Constants for GitHub integration
GITHUB_USER = "hawkarabdulhaq"
GITHUB_REPO = "energyscan"
JSON_FILE = "data/routine.json"
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


def classify_routine(responses):
    """Classify routine management based on survey responses."""
    score = 0

    # Assign weights for each response
    score += 4 if responses["q1"] == "Yes" else 2
    score += responses["q2"]
    score += responses["q3"]
    strategy_scores = {"A. Prioritize tasks.": 4, "B. Delegate tasks.": 3, "C. Reschedule activities.": 2, "D. Skip low-priority tasks.": 1}
    score += sum(strategy_scores.get(strategy, 0) for strategy in responses["q4"])
    score += 4 if responses["q5"] == "Yes" else 2
    score += responses["q6"]
    score += 4 if responses["q7"] == "Yes" else 2

    # Classify based on score
    if score >= 35:
        classification = "🎯 Highly consistent and adaptable routines with a focus on self-care and improvement."
    elif 28 <= score < 35:
        classification = "✅ Good routine management but with room for better adaptability and self-care."
    elif 20 <= score < 28:
        classification = "⚠️ Mixed routines, with gaps in consistency and self-care."
    else:
        classification = "❌ Lacks consistent routines and adaptability; needs significant improvements."

    return classification, score


def analyze_responses(responses):
    """Analyze individual responses and identify strengths and areas for improvement."""
    good = []
    improvement = []

    # Strengths
    if responses["q1"] == "Yes":
        good.append("You follow a structured daily routine.")
    if responses["q2"] >= 4:
        good.append("You stick to your daily schedule effectively.")
    if responses["q3"] >= 4:
        good.append("You adapt quickly to unexpected changes in your routine.")
    if "A. Prioritize tasks." in responses["q4"] or "B. Delegate tasks." in responses["q4"]:
        good.append("You use effective strategies to handle changes in your routine.")
    if responses["q5"] == "Yes":
        good.append("You intentionally allocate time for self-care.")
    if responses["q6"] >= 4:
        good.append("You are consistent in taking short breaks during work hours.")
    if responses["q7"] == "Yes":
        good.append("You regularly review your routine to improve its effectiveness.")

    # Areas for Improvement
    if responses["q1"] == "No":
        improvement.append("Consider adopting a structured daily routine to enhance consistency.")
    if responses["q2"] < 3:
        improvement.append("Work on sticking to your daily schedule more consistently.")
    if responses["q3"] < 3:
        improvement.append("Improve your ability to adapt to unexpected changes in your routine.")
    if "C. Reschedule activities." in responses["q4"] or "D. Skip low-priority tasks." in responses["q4"]:
        improvement.append("Focus on prioritizing tasks and delegating effectively during routine changes.")
    if responses["q5"] == "No":
        improvement.append("Ensure that you allocate time for self-care activities like exercise or relaxation.")
    if responses["q6"] < 3:
        improvement.append("Make a habit of taking regular breaks during work hours to recharge.")
    if responses["q7"] == "No":
        improvement.append("Review your routine periodically to identify areas for improvement.")

    return good, improvement


def display_routine_analysis():
    st.title("📊 Routine Analysis")
    st.markdown("""
    **Evaluate Your Routine Management**  
    This section analyzes your responses to the Routine Survey to identify strengths and areas for improvement.
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
        format_func=lambda i: f"Response {i + 1}",
        key="routine_response_select"
    )
    selected_response = data[selected_index]["responses"]

    # Display classification
    classification, total_score = classify_routine(selected_response)
    st.subheader("📋 Classification Results")
    st.info(f"**Classification:** {classification}")
    st.metric("Total Score", f"{total_score}/40")

    # Visualization of Score Distribution
    st.markdown("### 📊 Score Distribution")
    score_categories = ["Consistency", "Adaptability", "Self-Care", "Reflection"]
    scores = [
        selected_response["q2"],
        selected_response["q3"],
        selected_response["q6"],
        4 if selected_response["q7"] == "Yes" else 2
    ]
    fig = px.bar(x=score_categories, y=scores, labels={"x": "Category", "y": "Score"}, title="Score Distribution")
    st.plotly_chart(fig, use_container_width=True)

    # Display analysis
    st.subheader("📋 Analysis Results")
    good, improvement = analyze_responses(selected_response)

    # Strengths
    st.markdown("#### ✅ What is Good")
    if good:
        for item in good:
            st.write(f"- {item}")
    else:
        st.write("No significant strengths identified.")

    # Areas for Improvement
    st.markdown("#### 🔍 What Needs Improvement")
    if improvement:
        for item in improvement:
            st.write(f"- {item}")
    else:
        st.success("No significant areas for improvement were identified.")
