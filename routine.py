import streamlit as st
import json
import requests
import base64

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
    commit_message = "Update routine.json with new responses"

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


def routine_test():
    st.title("🛠️ Routine Test")
    st.markdown("""
    **Evaluate your consistency, resilience, adaptability, and self-care in daily routines.**
    """)

    # Initialize session state for responses
    if "routine_responses" not in st.session_state:
        st.session_state["routine_responses"] = {
            "q1": None,
            "q2": 3,
            "q3": 3,
            "q4": [],
            "q5": None,
            "q6": 3,
            "q7": None,
        }

    # Section 1: Consistency in Habits
    st.subheader("1️⃣ Consistency in Habits")
    st.session_state["routine_responses"]["q1"] = st.radio(
        "Do you follow a structured daily routine?",
        ["Yes", "No"],
        index=0 if st.session_state["routine_responses"]["q1"] == "Yes" else 1,
        key="routine_q1"
    )

    st.session_state["routine_responses"]["q2"] = st.slider(
        "How often do you stick to your daily schedule?",
        min_value=1,
        max_value=5,
        value=st.session_state.get("routine_responses", {}).get("q2", 3),
        format="Level %d",
        key="routine_q2"
    )

    # Section 2: Adaptability
    st.subheader("2️⃣ Adaptability Under Pressure")
    st.session_state["routine_responses"]["q3"] = st.slider(
        "How quickly do you adapt to unexpected changes in your routine?",
        min_value=1,
        max_value=5,
        value=st.session_state.get("routine_responses", {}).get("q3", 3),
        format="Level %d",
        key="routine_q3"
    )

    st.session_state["routine_responses"]["q4"] = st.multiselect(
        "What strategies do you use when adapting to changes?",
        ["A. Prioritize tasks.", "B. Delegate tasks.", "C. Reschedule activities.", "D. Skip low-priority tasks."],
        default=st.session_state["routine_responses"]["q4"],
        key="routine_q4"
    )

    # Section 3: Self-Care Integration
    st.subheader("3️⃣ Self-Care Integration")
    st.session_state["routine_responses"]["q5"] = st.radio(
        "Do you intentionally allocate time for self-care (e.g., exercise, relaxation)?",
        ["Yes", "No"],
        index=0 if st.session_state["routine_responses"]["q5"] == "Yes" else 1,
        key="routine_q5"
    )

    st.session_state["routine_responses"]["q6"] = st.slider(
        "How consistent are you in taking short breaks during work hours?",
        min_value=1,
        max_value=5,
        value=st.session_state.get("routine_responses", {}).get("q6", 3),
        format="Level %d",
        key="routine_q6"
    )

    # Section 4: Reflecting on Improvement
    st.subheader("4️⃣ Reflection and Improvement")
    st.session_state["routine_responses"]["q7"] = st.radio(
        "Do you review your routine regularly to improve its effectiveness?",
        ["Yes", "No"],
        index=0 if st.session_state["routine_responses"]["q7"] == "Yes" else 1,
        key="routine_q7"
    )

    # Submit Button
    if st.button("Submit Test", key="routine_submit"):
        responses = st.session_state["routine_responses"]
        score = 0
        score += 4 if responses["q1"] == "Yes" else 2
        score += responses["q2"]
        score += responses["q3"]
        strategy_scores = {"A. Prioritize tasks.": 4, "B. Delegate tasks.": 3, "C. Reschedule activities.": 2, "D. Skip low-priority tasks.": 1}
        score += sum(strategy_scores[strategy] for strategy in responses["q4"])
        score += 4 if responses["q5"] == "Yes" else 2
        score += responses["q6"]
        score += 4 if responses["q7"] == "Yes" else 2

        save_results_to_github({"score": score, "responses": responses})
        st.success("Your results have been saved successfully!")
