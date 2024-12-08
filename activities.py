import streamlit as st
import json
import requests
import base64

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
                st.error("Failed to decode existing data. Initializing as an empty list.")
                return []
    elif response.status_code == 404:
        st.warning("No existing data found. A new file will be created.")
        return []
    else:
        st.error(f"Failed to fetch data from GitHub. Error {response.status_code}: {response.text}")
        return []


def save_results_to_github(data):
    """Save or update data in the GitHub repository."""
    github_pat = get_github_pat()
    if not github_pat:
        return

    existing_data = load_existing_data()
    existing_data.append(data)

    headers = {
        "Authorization": f"token {github_pat}",
        "Accept": "application/vnd.github.v3+json",
    }

    # Encode content and prepare payload
    encoded_content = base64.b64encode(json.dumps(existing_data, indent=4).encode("utf-8")).decode("utf-8")
    commit_message = "Update activities.json with new responses"

    # Get the SHA of the existing file (if exists)
    sha = None
    response = requests.get(GITHUB_API_URL_JSON, headers=headers)
    if response.status_code == 200:
        sha = response.json().get("sha", None)

    payload = {"message": commit_message, "content": encoded_content}
    if sha:
        payload["sha"] = sha

    # Save the updated file
    save_response = requests.put(GITHUB_API_URL_JSON, headers=headers, json=payload)

    if save_response.status_code in [200, 201]:
        st.success("Results successfully saved to GitHub!")
    else:
        st.error(f"Failed to save results to GitHub. Error {save_response.status_code}: {save_response.text}")


def activities_test():
    st.title("🎯 Activities Test")
    st.markdown("""
    **Evaluate your task prioritization, clarity of goals, and focus.**
    Answer questions to identify opportunities to optimize your productivity.
    """)

    # Initialize session state for responses
    if "activities_responses" not in st.session_state:
        st.session_state["activities_responses"] = {
            "q1": "Always",
            "q2": False,
            "q3": 3,
            "q4": "Yes",
            "q5": [],
            "q6": "Always",
            "q7": 3,
        }

    # Section 1: Task Prioritization
    st.subheader("1️⃣ Task Prioritization")
    st.session_state["activities_responses"]["q1"] = st.radio(
        "How often do you prioritize tasks based on their importance?",
        ["Always", "Often", "Rarely", "Never"],
        index=["Always", "Often", "Rarely", "Never"].index(st.session_state["activities_responses"]["q1"]),
        key="activities_q1"
    )

    st.session_state["activities_responses"]["q2"] = st.checkbox(
        "Do you create a to-do list every morning to organize your day?",
        value=st.session_state["activities_responses"]["q2"],
        key="activities_q2"
    )

    # Section 2: Clarity of Goals
    st.subheader("2️⃣ Clarity of Goals")
    st.session_state["activities_responses"]["q3"] = st.slider(
        "On a scale of 1 to 5, how clear are your long-term goals?",
        min_value=1,
        max_value=5,
        value=st.session_state["activities_responses"]["q3"],
        format="Level %d",
        key="activities_q3"
    )

    st.session_state["activities_responses"]["q4"] = st.radio(
        "Do you break down large tasks into smaller, actionable steps?",
        ["Yes", "No"],
        index=0 if st.session_state["activities_responses"]["q4"] == "Yes" else 1,
        key="activities_q4"
    )

    # Section 3: Awareness of Impact
    st.subheader("3️⃣ Awareness of Impact")
    st.session_state["activities_responses"]["q5"] = st.multiselect(
        "What strategies do you use to evaluate the impact of your tasks?",
        [
            "Write down expected outcomes for each task.",
            "Compare task outcomes with goals.",
            "Use a decision-making framework.",
            "Complete tasks randomly without evaluation.",
        ],
        default=st.session_state["activities_responses"]["q5"],
        key="activities_q5"
    )

    # Section 4: Productivity and Focus
    st.subheader("4️⃣ Productivity and Focus")
    st.session_state["activities_responses"]["q6"] = st.radio(
        "When working on high-priority tasks, how often do you eliminate distractions?",
        ["Always", "Often", "Rarely", "Never"],
        index=["Always", "Often", "Rarely", "Never"].index(st.session_state["activities_responses"]["q6"]),
        key="activities_q6"
    )

    st.session_state["activities_responses"]["q7"] = st.slider(
        "How frequently do you review your goals and progress?",
        min_value=1,
        max_value=5,
        value=st.session_state["activities_responses"]["q7"],
        format="Level %d",
        key="activities_q7"
    )

    # Submit Test
    if st.button("Submit Test", key="activities_submit"):
        responses = st.session_state["activities_responses"]
        score = 0
        score += 4 if responses["q1"] == "Always" else 3 if responses["q1"] == "Often" else 2 if responses["q1"] == "Rarely" else 1
        score += 4 if responses["q2"] else 2
        score += responses["q3"]
        score += 4 if responses["q4"] == "Yes" else 2
        score += sum([4, 3, 2, 1][["Write down expected outcomes for each task.",
                                   "Compare task outcomes with goals.",
                                   "Use a decision-making framework.",
                                   "Complete tasks randomly without evaluation."].index(strategy)] for strategy in responses["q5"])
        score += 4 if responses["q6"] == "Always" else 3 if responses["q6"] == "Often" else 2 if responses["q6"] == "Rarely" else 1
        score += responses["q7"]

        save_results_to_github({"score": score, "responses": responses})
        st.success("Your results have been saved successfully!")
