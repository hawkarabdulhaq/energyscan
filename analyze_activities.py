import streamlit as st
import requests
import json
import base64
import plotly.express as px

# Constants for GitHub integration
GITHUB_USER = "hawkarabdulhaq"
GITHUB_REPO = "energyscan"
JSON_FILE = "data/activities.json"
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


def classify_activities(responses):
    """Classify activities management based on responses."""
    score = 0
    score += 4 if responses["q1"] == "Always" else 3 if responses["q1"] == "Often" else 2 if responses["q1"] == "Rarely" else 1
    score += 4 if responses["q2"] else 2
    score += int(responses["q3"])
    score += 4 if responses["q4"] == "Yes" else 2
    score += sum([4, 3, 2, 1][["Write down expected outcomes for each task.",
                               "Compare task outcomes with goals.",
                               "Use a decision-making framework.",
                               "Complete tasks randomly without evaluation."].index(strategy)] for strategy in responses.get("q5", []))
    score += 4 if responses["q6"] == "Always" else 3 if responses["q6"] == "Often" else 2 if responses["q6"] == "Rarely" else 1
    score += int(responses["q7"])

    # Classify based on score
    if score >= 40:
        classification = "🎯 Excellent task prioritization and focus."
    elif 30 <= score < 40:
        classification = "✅ Good practices but room for optimization."
    elif 20 <= score < 30:
        classification = "⚠️ Moderate task management, with opportunities to improve focus."
    else:
        classification = "❌ Significant improvements needed in task prioritization and productivity."

    return classification, score


def analyze_responses(responses):
    """Analyze individual responses and identify strengths and areas for improvement."""
    good = []
    improvement = []

    # Strengths
    if responses["q1"] in ["Always", "Often"]:
        good.append("You frequently prioritize tasks based on importance.")
    if responses["q2"]:
        good.append("You organize your day with a to-do list.")
    if responses["q3"] >= 4:
        good.append("You have clear long-term goals.")
    if responses["q4"] == "Yes":
        good.append("You break down large tasks into smaller, actionable steps.")
    if "Write down expected outcomes for each task." in responses.get("q5", []):
        good.append("You evaluate tasks by writing down expected outcomes.")
    if responses["q6"] in ["Always", "Often"]:
        good.append("You eliminate distractions while working on high-priority tasks.")
    if responses["q7"] >= 4:
        good.append("You frequently review your goals and progress.")

    # Areas for Improvement
    if responses["q1"] in ["Rarely", "Never"]:
        improvement.append("Focus on prioritizing tasks based on their importance.")
    if not responses["q2"]:
        improvement.append("Consider using a to-do list to organize your day.")
    if responses["q3"] <= 2:
        improvement.append("Work on clarifying your long-term goals.")
    if responses["q4"] == "No":
        improvement.append("Break down large tasks into smaller, actionable steps.")
    if not responses.get("q5"):
        improvement.append("Adopt strategies to evaluate the impact of tasks.")
    if responses["q6"] in ["Rarely", "Never"]:
        improvement.append("Eliminate distractions when working on high-priority tasks.")
    if responses["q7"] <= 2:
        improvement.append("Review your goals and progress more frequently.")

    return good, improvement


def display_activities_analysis():
    st.title("📊 Activities Analysis")
    st.markdown("""
    **Analyze Your Activities**  
    This section evaluates your responses to the Activities Survey to highlight strengths and areas for improvement.
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
        key="activities_response_select"
    )
    selected_response = data[selected_index]["responses"]

    # Display classification
    classification, total_score = classify_activities(selected_response)
    st.subheader("📋 Classification Results")
    st.info(f"**Classification:** {classification}")
    st.metric("Total Score", f"{total_score}/50")

    # Visualization of Score Distribution
    st.markdown("### 📊 Score Distribution")
    score_categories = ["Task Prioritization", "Clarity of Goals", "Focus & Productivity"]
    scores = [
        4 if selected_response["q1"] == "Always" else 3 if selected_response["q1"] == "Often" else 2,
        int(selected_response["q3"]),
        int(selected_response["q7"]),
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
