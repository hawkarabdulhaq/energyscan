import streamlit as st
import json
import requests
import base64
import pandas as pd
import plotly.express as px

# Constants for GitHub integration
GITHUB_USER = "hawkarabdulhaq"
GITHUB_REPO = "energyscan"

FILES = {
    "Awareness": "data/awareness.json",
    "Routine": "data/routine.json",
    "Well-being": "data/wellbeing.json",
    "Activities": "data/activities.json",
}

def get_github_pat():
    """Retrieve GitHub PAT from Streamlit secrets."""
    try:
        return st.secrets["github_pat"]
    except KeyError:
        st.error("GitHub PAT not found in secrets! Please add `github_pat` to your secrets.")
        return None


def load_data(file_name):
    """Load data from GitHub repository."""
    github_pat = get_github_pat()
    if not github_pat:
        return []

    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{file_name}"
    headers = {"Authorization": f"token {github_pat}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        content = response.json().get("content", "")
        if content:
            try:
                return json.loads(base64.b64decode(content).decode("utf-8"))
            except json.JSONDecodeError:
                st.error(f"Failed to decode {file_name}. Returning an empty list.")
                return []
    elif response.status_code == 404:
        return []
    else:
        st.error(f"Failed to fetch {file_name}. Error {response.status_code}: {response.text}")
        return []


def categorize_user(total_score):
    """Categorize user based on total score."""
    if total_score >= 180:
        return "🌟 Energy Leader", "Excellent performance across all categories."
    elif 120 <= total_score < 180:
        return "📈 Focused Improver", "Good performance but room for improvement."
    else:
        return "🔍 Energy Explorer", "Develop awareness and management strategies."


def display_results():
    st.title("📈 Results Dashboard")
    st.markdown("**Here’s a summary of your energy performance across all surveys.**")

    # Load data from all JSON files
    results = {}
    for category, file_name in FILES.items():
        data = load_data(file_name)
        scores = [entry["score"] for entry in data] if data else [0]
        results[category] = sum(scores) / len(scores) if scores else 0

    # Calculate total and average scores
    total_score = sum(results.values())
    avg_score = total_score / len(FILES)

    # Categorize user
    category, message = categorize_user(total_score)

    # Display overall results
    st.subheader("📊 Your Overall Performance")
    st.metric("Total Score", f"{total_score} / 200")
    st.metric("Average Score", f"{avg_score:.2f} / 50")
    st.info(f"**Category:** {category}\n\n{message}")

    # Display detailed breakdown
    st.subheader("📋 Score Breakdown by Survey")
    score_df = pd.DataFrame(results.items(), columns=["Survey", "Score"])
    fig = px.bar(score_df, x="Survey", y="Score", title="Scores by Survey", color="Survey", text="Score")
    st.plotly_chart(fig, use_container_width=True)

    # Strengths and improvement areas
    st.subheader("✅ Strengths and Opportunities")
    strengths = [f"- **{survey}**: Excellent score of {score}" for survey, score in results.items() if score >= 40]
    improvements = [f"- **{survey}**: Needs improvement (Score: {score})" for survey, score in results.items() if score < 30]

    if strengths:
        st.markdown("### ✅ Strengths")
        for strength in strengths:
            st.markdown(strength)
    if improvements:
        st.markdown("### ⚠️ Areas for Improvement")
        for improvement in improvements:
            st.markdown(improvement)

    # Placeholder for report download (future enhancement)
    st.subheader("📥 Report Download")
    st.info("🚀 Downloadable reports coming soon!")
