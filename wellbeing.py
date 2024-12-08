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
            "q3": 3,
            "q4": None,
            "q5": None,
            "q6": 3,
            "q7": [],
            "q8": 3,
            "q9": None,
        }

    # Section 1: Work-Life Balance
    st.subheader("1️⃣ Work-Life Balance")
    st.session_state["wellbeing_responses"]["q1"] = st.radio(
        "Do you feel you have a healthy balance between work and personal life?",
        ["Yes", "No"],
        index=0 if st.session_state["wellbeing_responses"]["q1"] == "Yes" else 1,
        key="wellbeing_q1"
    )

    st.session_state["wellbeing_responses"]["q2"] = st.radio(
        "Do you dedicate specific time daily for personal activities like hobbies or relaxation?",
        ["Yes", "No"],
        index=0 if st.session_state["wellbeing_responses"]["q2"] == "Yes" else 1,
        key="wellbeing_q2"
    )

    # Section 2: Physical and Mental Well-being
    st.subheader("2️⃣ Physical and Mental Well-being")
    st.session_state["wellbeing_responses"]["q3"] = st.slider(
        "On a scale of 1 to 5, how consistent are you with maintaining a healthy lifestyle (e.g., diet, exercise)?",
        min_value=1,
        max_value=5,
        value=st.session_state["wellbeing_responses"]["q3"],
        format="Level %d",
        key="wellbeing_q3"
    )

    st.session_state["wellbeing_responses"]["q4"] = st.radio(
        "Do you practice mindfulness or stress-relief techniques regularly?",
        ["Yes", "No"],
        index=0 if st.session_state["wellbeing_responses"]["q4"] == "Yes" else 1,
        key="wellbeing_q4"
    )

    st.session_state["wellbeing_responses"]["q5"] = st.radio(
        "How often do you feel mentally drained by the end of the day?",
        [
            "Rarely, I manage my mental energy well.",
            "Occasionally, but it’s manageable.",
            "Frequently, it impacts my productivity.",
            "Almost always, I feel exhausted."
        ],
        index={
            "Rarely, I manage my mental energy well.": 0,
            "Occasionally, but it’s manageable.": 1,
            "Frequently, it impacts my productivity.": 2,
            "Almost always, I feel exhausted.": 3,
        }.get(st.session_state["wellbeing_responses"]["q5"], 0),
        key="wellbeing_q5"
    )

    # Section 3: Social Well-being
    st.subheader("3️⃣ Social Well-being")
    st.session_state["wellbeing_responses"]["q6"] = st.slider(
        "On a scale of 1 to 5, how connected do you feel with your family and friends?",
        min_value=1,
        max_value=5,
        value=st.session_state["wellbeing_responses"]["q6"],
        format="Level %d",
        key="wellbeing_q6"
    )

    st.session_state["wellbeing_responses"]["q7"] = st.multiselect(
        "What activities do you engage in to build social connections?",
        [
            "A. Weekly family meetups.",
            "B. Socializing with friends.",
            "C. Community or volunteering work.",
            "D. Online groups or chats."
        ],
        default=st.session_state["wellbeing_responses"]["q7"],
        key="wellbeing_q7"
    )

    # Section 4: Self-Reflection
    st.subheader("4️⃣ Self-Reflection")
    st.session_state["wellbeing_responses"]["q8"] = st.slider(
        "How satisfied are you with your current work-life balance?",
        min_value=1,
        max_value=5,
        value=st.session_state["wellbeing_responses"]["q8"],
        format="Level %d",
        key="wellbeing_q8"
    )

    st.session_state["wellbeing_responses"]["q9"] = st.radio(
        "Do you actively evaluate your well-being and make adjustments as needed?",
        ["Yes", "No"],
        index=0 if st.session_state["wellbeing_responses"]["q9"] == "Yes" else 1,
        key="wellbeing_q9"
    )

    # Submit Test
    if st.button("Submit Test", key="wellbeing_submit"):
        responses = st.session_state["wellbeing_responses"]
        score = 0
        score += 4 if responses["q1"] == "Yes" else 2
        score += 4 if responses["q2"] == "Yes" else 2
        score += responses["q3"]
        score += 4 if responses["q4"] == "Yes" else 2
        score += {"Rarely, I manage my mental energy well.": 4, "Occasionally, but it’s manageable.": 3, "Frequently, it impacts my productivity.": 2, "Almost always, I feel exhausted.": 1}[responses["q5"]]
        score += responses["q6"]
        score += len(responses["q7"]) * 2
        score += responses["q8"]
        score += 4 if responses["q9"] == "Yes" else 2

        save_results_to_github({"score": score, "responses": responses})
        st.success("Your results have been saved successfully!")
