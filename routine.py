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
            "q3": None,
            "q4": None,
            "q5": [],
            "q6": 3,
            "q7": None,
            "q8": "",
            "q9": 3,
        }

    # Section 1: Consistency in Habits
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

    st.session_state["routine_responses"]["q2"] = st.slider(
        "How frequently do you plan your daily schedule in advance?",
        min_value=1,
        max_value=5,
        value=st.session_state["routine_responses"]["q2"],
        format="Level %d (1 = Never, 5 = Always)",
        key="routine_q2"
    )

    # Section 2: Resilience Under Pressure
    st.subheader("2️⃣ Resilience Under Pressure")
    st.session_state["routine_responses"]["q3"] = st.radio(
        "How do you respond to unexpected challenges?",
        ["A. Adapt quickly and find solutions.",
         "B. Take time to adapt but recover.",
         "C. Struggle to cope and feel overwhelmed.",
         "D. Avoid challenges and feel stuck."],
        index={
            "A": 0, "B": 1, "C": 2, "D": 3
        }[st.session_state["routine_responses"]["q3"][0]] if st.session_state["routine_responses"]["q3"] else 0,
        key="routine_q3"
    )

    st.session_state["routine_responses"]["q4"] = st.multiselect(
        "What strategies do you use to manage setbacks in your plans?",
        ["A. Reflect and adjust strategies.",
         "B. Seek help or resources.",
         "C. Take a break and return later.",
         "D. Ignore the setback and move on."],
        default=st.session_state["routine_responses"]["q4"],
        key="routine_q4"
    )

    # Section 3: Adaptability
    st.subheader("3️⃣ Adaptability")
    st.session_state["routine_responses"]["q5"] = st.text_input(
        "What is your biggest challenge when adapting to new routines?",
        value=st.session_state["routine_responses"]["q5"],
        key="routine_q5"
    )

    st.session_state["routine_responses"]["q6"] = st.slider(
        "How comfortable are you with changing habits to meet goals?",
        min_value=1,
        max_value=5,
        value=st.session_state["routine_responses"]["q6"],
        format="Level %d (1 = Uncomfortable, 5 = Very Comfortable)",
        key="routine_q6"
    )

    # Section 4: Self-Care
    st.subheader("4️⃣ Self-Care")
    st.session_state["routine_responses"]["q7"] = st.radio(
        "Do you prioritize self-care in your daily routine?",
        ["Yes", "No"],
        index=0 if st.session_state["routine_responses"]["q7"] == "Yes" else 1,
        key="routine_q7"
    )

    st.session_state["routine_responses"]["q8"] = st.text_area(
        "Describe one routine that helps you recharge during stressful times:",
        value=st.session_state["routine_responses"]["q8"],
        key="routine_q8"
    )

    st.session_state["routine_responses"]["q9"] = st.slider(
        "How effective is your current routine in balancing work and personal life?",
        min_value=1,
        max_value=5,
        value=st.session_state["routine_responses"]["q9"],
        format="Level %d (1 = Poor, 5 = Excellent)",
        key="routine_q9"
    )

    # Submit Button
    if st.button("Submit Test", key="routine_submit"):
        responses = st.session_state["routine_responses"]
        score = 0
        score += {"A": 4, "B": 3, "C": 2, "D": 1}[responses["q1"][0]]
        score += responses["q2"]
        score += {"A": 4, "B": 3, "C": 2, "D": 1}[responses["q3"][0]]
        strategy_scores = {"A. Reflect and adjust strategies.": 4,
                           "B. Seek help or resources.": 3,
                           "C. Take a break and return later.": 2,
                           "D. Ignore the setback and move on.": 1}
        score += sum(strategy_scores[strategy] for strategy in responses["q4"])
        score += responses["q6"]
        score += 4 if responses["q7"] == "Yes" else 2
        score += responses["q9"]

        save_results_to_github({"score": score, "responses": responses})
        st.success("Your results have been saved successfully!")
