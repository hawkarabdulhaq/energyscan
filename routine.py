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
            "q2": None,
            "q3": None,
            "q4": None,
        }

    # Question 1
    st.subheader("1️⃣ Consistency in Habits")
    st.session_state["routine_responses"]["q1"] = st.radio(
        "How consistent are you in maintaining daily routines?",
        ["A. Extremely consistent, I rarely miss a day.",
         "B. Fairly consistent, but I occasionally skip.",
         "C. Inconsistent, I struggle to maintain routines.",
         "D. Not consistent at all."],
        index={
            "A": 0, "B": 1, "C": 2, "D": 3
        }[st.session_state["routine_responses"]["q1"][0]] if st.session_state["routine_responses"]["q1"] else 0,
        key="routine_q1"
    )

    # Question 2
    st.session_state["routine_responses"]["q2"] = st.radio(
        "How often do you review and adapt your habits based on changing circumstances?",
        ["A. Regularly, I reflect and adjust proactively.",
         "B. Occasionally, when I feel the need for improvement.",
         "C. Rarely, I resist changing routines.",
         "D. Never, I stick to the same habits regardless of outcomes."],
        index={
            "A": 0, "B": 1, "C": 2, "D": 3
        }[st.session_state["routine_responses"]["q2"][0]] if st.session_state["routine_responses"]["q2"] else 0,
        key="routine_q2"
    )

    # Question 3
    st.subheader("2️⃣ Resilience Under Pressure")
    st.session_state["routine_responses"]["q3"] = st.radio(
        "When faced with unexpected challenges, how do you respond?",
        ["A. I adjust quickly and stay focused on my goals.",
         "B. I adapt eventually but feel stressed initially.",
         "C. I struggle to find my footing and often feel overwhelmed.",
         "D. I avoid addressing challenges and feel stuck."],
        index={
            "A": 0, "B": 1, "C": 2, "D": 3
        }[st.session_state["routine_responses"]["q3"][0]] if st.session_state["routine_responses"]["q3"] else 0,
        key="routine_q3"
    )

    # Question 4
    st.session_state["routine_responses"]["q4"] = st.radio(
        "How do you handle setbacks in your plans or goals?",
        ["A. I reflect, learn, and create new plans quickly.",
         "B. I recover eventually but dwell on the setback for some time.",
         "C. I find it difficult to recover and lose momentum.",
         "D. I often abandon goals after setbacks."],
        index={
            "A": 0, "B": 1, "C": 2, "D": 3
        }[st.session_state["routine_responses"]["q4"][0]] if st.session_state["routine_responses"]["q4"] else 0,
        key="routine_q4"
    )

    # Submit Button
    if st.button("Submit Test", key="routine_submit"):
        responses = st.session_state["routine_responses"]
        score = 0
        score += {"A": 4, "B": 3, "C": 2, "D": 1}[responses["q1"][0]]
        score += {"A": 4, "B": 3, "C": 2, "D": 1}[responses["q2"][0]]
        score += {"A": 4, "B": 3, "C": 2, "D": 1}[responses["q3"][0]]
        score += {"A": 4, "B": 3, "C": 2, "D": 3}[responses["q4"][0]]

        save_results_to_github({"score": score, "responses": responses})
        st.success("Your results have been saved successfully!")
