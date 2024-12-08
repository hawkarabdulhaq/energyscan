import streamlit as st
import json
import requests
import base64

# GitHub Repository Details
GITHUB_USER = "hawkarabdulhaq"
GITHUB_REPO = "energyscan"
GITHUB_PAT = st.secrets["github_pat"]  # GitHub Personal Access Token
FILE_PATH = "data/awareness.json"

def fetch_existing_data():
    """Fetch existing data from the GitHub repository."""
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{FILE_PATH}"
    headers = {
        "Authorization": f"Bearer {GITHUB_PAT}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        content = response.json().get("content", "")
        if content:
            return json.loads(base64.b64decode(content).decode("utf-8")), response.json()["sha"]
        else:
            return [], None
    elif response.status_code == 404:
        return [], None
    else:
        st.error(f"Failed to fetch data from GitHub. Error {response.status_code}: {response.json().get('message')}")
        return None, None

def save_data_to_github(data):
    """Save or update data in the GitHub repository."""
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{FILE_PATH}"
    headers = {
        "Authorization": f"Bearer {GITHUB_PAT}",
        "Accept": "application/vnd.github.v3+json",
    }

    existing_data, sha = fetch_existing_data()
    if existing_data is None:
        return

    # Append new data
    existing_data.append(data)

    # Prepare payload
    encoded_content = base64.b64encode(json.dumps(existing_data, indent=4).encode("utf-8")).decode("utf-8")
    payload = {
        "message": "Update awareness.json with new data",
        "content": encoded_content,
    }
    if sha:
        payload["sha"] = sha

    # Make the API request
    response = requests.put(url, headers=headers, json=payload)

    if response.status_code in [200, 201]:
        st.success("Your results have been saved successfully to GitHub!")
    else:
        st.error(f"Failed to save data to GitHub. Error {response.status_code}: {response.json().get('message')}")

def awareness_test():
    st.title("Energy Awareness Test")
    st.markdown("**Answer the following questions to assess your energy performance level.**")

    # Initialize session state for responses
    if "awareness_responses" not in st.session_state:
        st.session_state["awareness_responses"] = {
            "q1": None,
            "q2": 3,
            "q3": None,
            "q4": 3,
            "q5": [],
            "q6": None,
            "q7": 3,
            "q8": None,
            "q9": 3,
        }

    # Section 1: Awareness
    st.subheader("Section 1: Awareness")
    st.session_state["awareness_responses"]["q1"] = st.radio(
        "Do you feel you understand your natural energy highs and lows during the day?",
        ["Yes", "No"],
        index=0 if st.session_state["awareness_responses"]["q1"] == "Yes" else 1,
        key="awareness_q1",
    )

    st.session_state["awareness_responses"]["q2"] = st.slider(
        "How well can you predict your peak energy times during the day?",
        min_value=1,
        max_value=5,
        value=st.session_state["awareness_responses"]["q2"],
        format="Level %d",
        key="awareness_q2",
    )

    st.session_state["awareness_responses"]["q3"] = st.radio(
        "How do you become aware of your energy levels?",
        [
            "A. Through regular tracking or journaling.",
            "B. Occasionally reflect on energy levels.",
            "C. Only notice during extreme highs/lows.",
            "D. Rarely think about energy levels.",
        ],
        index={
            "A": 0,
            "B": 1,
            "C": 2,
            "D": 3,
        }.get(st.session_state["awareness_responses"]["q3"][0], 0) if st.session_state["awareness_responses"]["q3"] else 0,
        key="awareness_q3",
    )

    # Section 2: Task Alignment
    st.subheader("Section 2: Task Alignment")
    st.session_state["awareness_responses"]["q4"] = st.slider(
        "How often do you schedule demanding tasks during your peak energy hours?",
        min_value=1,
        max_value=5,
        value=st.session_state["awareness_responses"]["q4"],
        format="Level %d",
        key="awareness_q4",
    )

    st.session_state["awareness_responses"]["q5"] = st.multiselect(
        "What strategies do you use to handle tasks during low energy periods?",
        [
            "A. Adjust tasks to match energy levels.",
            "B. Take a short break or recharge.",
            "C. Push through regardless.",
            "D. Delay tasks until later.",
        ],
        default=st.session_state["awareness_responses"]["q5"],
        key="awareness_q5",
    )

    # Section 3: Consistency and Habits
    st.subheader("Section 3: Consistency and Habits")
    st.session_state["awareness_responses"]["q6"] = st.radio(
        "Do you maintain a consistent sleep schedule to optimize energy usage?",
        ["Yes", "No"],
        index=0 if st.session_state["awareness_responses"]["q6"] == "Yes" else 1,
        key="habits_q6",
    )

    st.session_state["awareness_responses"]["q7"] = st.slider(
        "How consistent are you in taking regular breaks during work hours?",
        min_value=1,
        max_value=5,
        value=st.session_state["awareness_responses"]["q7"],
        format="Level %d",
        key="habits_q7",
    )

    # Section 4: Self-Reflection
    st.subheader("Section 4: Self-Reflection")
    st.session_state["awareness_responses"]["q8"] = st.radio(
        "Do you feel in control of your energy usage daily?",
        ["Yes", "No"],
        index=0 if st.session_state["awareness_responses"]["q8"] == "Yes" else 1,
        key="reflection_q8",
    )

    st.session_state["awareness_responses"]["q9"] = st.slider(
        "How satisfied are you with your current energy management?",
        min_value=1,
        max_value=5,
        value=st.session_state["awareness_responses"]["q9"],
        format="Level %d",
        key="reflection_q9",
    )

    # Submit Test
    if st.button("Submit Test"):
        responses = st.session_state["awareness_responses"]
        score = 0
        score += 4 if responses["q1"] == "Yes" else 2
        score += responses["q2"]
        score += {"A": 4, "B": 3, "C": 2, "D": 1}[responses["q3"][0]]
        score += responses["q4"]
        strategy_scores = {
            "A. Adjust tasks to match energy levels.": 4,
            "B. Take a short break or recharge.": 3,
            "C. Push through regardless.": 2,
            "D. Delay tasks until later.": 1,
        }
        score += sum(strategy_scores[strategy] for strategy in responses["q5"])
        score += 4 if responses["q6"] == "Yes" else 2
        score += responses["q7"]
        score += 4 if responses["q8"] == "Yes" else 2
        score += responses["q9"]

        save_data_to_github({"score": score, "responses": responses})
