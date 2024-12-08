import streamlit as st
import requests
import json
import base64
import plotly.express as px

# Constants for GitHub integration
GITHUB_USER = "hawkarabdulhaq"
GITHUB_REPO = "energyscan"
JSON_FILE = "data/wellbeing.json"
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


def classify_wellbeing(responses):
    """Classify well-being based on survey responses."""
    score = 0
    score += 4 if responses["q1"] == "Yes" else 2
    score += 4 if responses["q2"] == "Yes" else 2
    score += responses["q3"]
    score += 4 if responses["q4"] == "Yes" else 2
    score += {"Rarely, I manage my mental energy well.": 4, 
              "Occasionally, but it’s manageable.": 3, 
              "Frequently, it impacts my productivity.": 2, 
              "Almost always, I feel exhausted.": 1}[responses["q5"]]
    score += responses["q6"]
    score += len(responses["q7"]) * 2
    score += responses["q8"]
    score += 4 if responses["q9"] == "Yes" else 2

    # Classify based on score
    if score >= 40:
        classification = "🎯 Excellent balance and self-care practices."
    elif 30 <= score < 40:
        classification = "✅ Good well-being practices but room for improvement."
    elif 20 <= score < 30:
        classification = "⚠️ Moderate well-being, with gaps in self-care and social connections."
    else:
        classification = "❌ Needs significant improvements in work-life balance and self-care."

    return classification, score


def analyze_responses(responses):
    """Analyze individual responses and identify strengths and areas for improvement."""
    good = []
    improvement = []

    # Strengths
    if responses["q1"] == "Yes":
        good.append("You maintain a healthy balance between work and personal life.")
    if responses["q2"] == "Yes":
        good.append("You dedicate time daily for personal activities like hobbies or relaxation.")
    if responses["q3"] >= 4:
        good.append("You are consistent in maintaining a healthy lifestyle (e.g., diet, exercise).")
    if responses["q4"] == "Yes":
        good.append("You practice mindfulness or stress-relief techniques regularly.")
    if responses["q5"] == "Rarely, I manage my mental energy well.":
        good.append("You effectively manage your mental energy throughout the day.")
    if responses["q6"] >= 4:
        good.append("You feel well-connected with your family and friends.")
    if responses["q7"]:
        good.append("You engage in activities to build social connections.")
    if responses["q8"] >= 4:
        good.append("You are satisfied with your current work-life balance.")
    if responses["q9"] == "Yes":
        good.append("You actively evaluate your well-being and make adjustments.")

    # Areas for Improvement
    if responses["q1"] == "No":
        improvement.append("Work on creating a healthier balance between work and personal life.")
    if responses["q2"] == "No":
        improvement.append("Dedicate time daily for personal activities like hobbies or relaxation.")
    if responses["q3"] < 3:
        improvement.append("Focus on maintaining a more consistent healthy lifestyle (e.g., diet, exercise).")
    if responses["q4"] == "No":
        improvement.append("Incorporate mindfulness or stress-relief techniques into your routine.")
    if responses["q5"] in ["Frequently, it impacts my productivity.", "Almost always, I feel exhausted."]:
        improvement.append("Find ways to manage mental energy better and reduce feelings of exhaustion.")
    if responses["q6"] < 3:
        improvement.append("Work on strengthening connections with family and friends.")
    if not responses["q7"]:
        improvement.append("Engage in activities that build social connections.")
    if responses["q8"] < 3:
        improvement.append("Improve satisfaction with your work-life balance by reflecting on priorities.")
    if responses["q9"] == "No":
        improvement.append("Regularly evaluate your well-being and make necessary adjustments.")

    return good, improvement


def display_wellbeing_analysis():
    st.title("📊 Well-being Analysis")
    st.markdown("""
    **Analyze Your Well-being**  
    This section evaluates your responses to the Well-being Survey to highlight strengths and areas for improvement.
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
        key="wellbeing_response_select"
    )
    selected_response = data[selected_index]["responses"]

    # Display classification
    classification, total_score = classify_wellbeing(selected_response)
    st.subheader("📋 Classification Results")
    st.info(f"**Classification:** {classification}")
    st.metric("Total Score", f"{total_score}/50")

    # Visualization of Score Distribution
    st.markdown("### 📊 Score Distribution")
    score_categories = ["Work-Life Balance", "Healthy Lifestyle", "Social Connection", "Reflection"]
    scores = [
        4 if selected_response["q1"] == "Yes" else 2,
        selected_response["q3"],
        selected_response["q6"],
        selected_response["q8"]
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
