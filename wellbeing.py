import streamlit as st
import json
import requests
import base64

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
    commit_message = "Update wellbeing.json with new responses"

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


def wellbeing_test():
    st.title("🌱 Well-being Test")
    st.markdown("""
    **Assess your balance between work, life, and self-care.**
    Answer questions to identify ways to improve physical and mental well-being.
    """)

    # Initialize session state for responses
    if "wellbeing_responses" not in st.session_state:
        st.session_state["wellbeing_responses"] = {
            "q1": None,
            "q2": None,
            "q3": None,
            "q4": None,
        }

    # Section 1: Work-Life Balance
    st.subheader("1️⃣ Work-Life Balance")
    st.session_state["wellbeing_responses"]["q1"] = st.radio(
        "How often do you set boundaries between work and personal time?",
        [
            "A. Always, I maintain clear boundaries.",
            "B. Often, but I occasionally let them overlap.",
            "C. Rarely, work often spills into personal time.",
            "D. Never, I struggle to separate the two."
        ],
        index={
            "A": 0, "B": 1, "C": 2, "D": 3
        }.get(st.session_state["wellbeing_responses"]["q1"], 0),
        key="wellbeing_q1"
    )

    st.session_state["wellbeing_responses"]["q2"] = st.radio(
        "Do you allocate time for activities that rejuvenate you (e.g., hobbies, relaxation)?",
        [
            "A. Always, I make it a priority.",
            "B. Often, but not consistently.",
            "C. Rarely, I find it hard to make time.",
            "D. Never, I’m too busy to focus on myself."
        ],
        index={
            "A": 0, "B": 1, "C": 2, "D": 3
        }.get(st.session_state["wellbeing_responses"]["q2"], 0),
        key="wellbeing_q2"
    )

    # Section 2: Physical and Mental Well-being
    st.subheader("2️⃣ Physical and Mental Well-being")
    st.session_state["wellbeing_responses"]["q3"] = st.radio(
        "How consistent are you in maintaining physical health (e.g., exercise, healthy diet)?",
        [
            "A. Very consistent, I prioritize my physical well-being.",
            "B. Fairly consistent, but I occasionally slip.",
            "C. Inconsistent, I struggle to maintain a routine.",
            "D. Not consistent at all."
        ],
        index={
            "A": 0, "B": 1, "C": 2, "D": 3
        }.get(st.session_state["wellbeing_responses"]["q3"], 0),
        key="wellbeing_q3"
    )

    st.session_state["wellbeing_responses"]["q4"] = st.radio(
        "How often do you take steps to manage stress (e.g., mindfulness, breaks, support)?",
        [
            "A. Always, I actively manage stress effectively.",
            "B. Often, but I could improve my strategies.",
            "C. Rarely, I manage stress reactively.",
            "D. Never, I feel overwhelmed most of the time."
        ],
        index={
            "A": 0, "B": 1, "C": 2, "D": 3
        }.get(st.session_state["wellbeing_responses"]["q4"], 0),
        key="wellbeing_q4"
    )

    # Submit Button
    if st.button("Submit Test", key="wellbeing_submit"):
        responses = st.session_state["wellbeing_responses"]
        score = sum(
            {"A": 4, "B": 3, "C": 2, "D": 1}[resp[0]]
            for resp in responses.values()
        )

        save_results_to_github({"score": score, "responses": responses})
        st.success("Your results have been saved successfully!")
