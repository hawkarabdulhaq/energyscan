import streamlit as st
import requests
import json
import base64
import plotly.express as px

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


def classify_responses(responses):
    """Classify the user's approach to task prioritization based on responses."""
    score = 0

    # Assign weights for each response
    score += 4 if responses["q1"] == "Yes" else 2
    score += responses["q2"]
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[responses["q3"][0]]
    score += responses["q4"]
    strategy_scores = {
        "A. Adjust tasks to match energy levels.": 4,
        "B. Take a short break or recharge.": 3,
        "C. Push through regardless.": 2,
        "D. Delay tasks until later.": 1
    }
    score += sum(strategy_scores[strategy] for strategy in responses["q5"])
    score += 4 if responses["q6"] == "Yes" else 2
    score += responses["q7"]
    score += 4 if responses["q8"] == "Yes" else 2
    score += responses["q9"]

    # Classify based on score
    if score >= 35:
        classification = "🎯 Prioritizes essential, goal-oriented activities with clear impact."
    elif 28 <= score < 35:
        classification = "✅ Focuses on impactful tasks most of the time but occasionally gets sidetracked."
    elif 20 <= score < 28:
        classification = "⚠️ Mixes impactful and trivial tasks, leading to diluted results."
    else:
        classification = "❌ Focuses primarily on low-value tasks; lacks clarity on priorities."

    return classification, score


def analyze_responses(responses):
    """Analyze individual responses and identify strengths and areas for improvement."""
    good = []
    improvement = []

    # Strengths
    if responses["q1"] == "Yes":
        good.append("You understand your natural energy highs and lows.")
    if responses["q2"] >= 4:
        good.append("You are good at predicting your peak energy times.")
    if responses["q3"].startswith("A") or responses["q3"].startswith("B"):
        good.append("You regularly reflect on your energy levels.")
    if responses["q4"] >= 4:
        good.append("You effectively schedule demanding tasks during your peak energy hours.")
    if "A. Adjust tasks to match energy levels." in responses["q5"] or "B. Take a short break or recharge." in responses["q5"]:
        good.append("You use effective strategies for managing low-energy periods.")
    if responses["q6"] == "Yes":
        good.append("You maintain a consistent sleep schedule.")
    if responses["q7"] >= 4:
        good.append("You take regular breaks during work hours.")
    if responses["q8"] == "Yes":
        good.append("You feel in control of your energy usage daily.")
    if responses["q9"] >= 4:
        good.append("You are satisfied with your current energy management practices.")

    # Areas for Improvement
    if responses["q1"] == "No":
        improvement.append("Work on understanding your natural energy highs and lows during the day.")
    if responses["q2"] < 3:
        improvement.append("Improve your ability to predict peak energy times by observing and journaling daily patterns.")
    if responses["q3"].startswith("D"):
        improvement.append("Regularly track your energy levels to increase awareness.")
    if responses["q4"] < 3:
        improvement.append("Consider scheduling demanding tasks during your peak energy hours for better productivity.")
    if "C. Push through regardless." in responses["q5"] or "D. Delay tasks until later." in responses["q5"]:
        improvement.append("Adopt better strategies for low-energy periods, such as taking breaks or reprioritizing tasks.")
    if responses["q6"] == "No":
        improvement.append("Maintain a consistent sleep schedule to enhance energy optimization.")
    if responses["q7"] < 3:
        improvement.append("Schedule regular breaks during work hours to recharge and sustain productivity.")
    if responses["q8"] == "No":
        improvement.append("Focus on techniques to feel more in control of your daily energy management.")
    if responses["q9"] < 3:
        improvement.append("Work on improving your satisfaction with your energy management by refining routines.")

    return good, improvement


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

    # Display classification
    classification, total_score = classify_responses(selected_response)
    st.subheader("📋 Classification Results")
    st.info(f"**Classification:** {classification}")
    st.metric("Total Score", f"{total_score}/40")

    # Visualization of Score Distribution
    st.markdown("### 📊 Score Distribution")
    score_categories = ["Energy Awareness", "Task Alignment", "Consistency", "Self-Reflection"]
    scores = [
        selected_response["q2"] + {"A": 4, "B": 3, "C": 2, "D": 1}[selected_response["q3"][0]],
        selected_response["q4"],
        selected_response["q7"],
        selected_response["q9"]
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

    # Display full response for context
    st.markdown("### 📄 Full Response Data")
    st.json(selected_response)
