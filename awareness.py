import streamlit as st
import json
import requests
import base64

# Constants for GitHub integration
GITHUB_USER = "habdulhaq87"
GITHUB_REPO = "energyscan"
JSON_FILE = "data/awareness.json"
GITHUB_API_URL_JSON = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{JSON_FILE}"

def get_github_pat():
    """Retrieve GitHub PAT from Streamlit secrets or notify the user."""
    try:
        return st.secrets["github_pat"]
    except KeyError:
        st.error("GitHub PAT not found in secrets! Please add `github_pat` to your secrets.")
        return None

def ensure_directory_exists():
    """Ensure the directory exists in the GitHub repository."""
    github_pat = get_github_pat()
    if not github_pat:
        return False

    directory_url = GITHUB_API_URL_JSON.rsplit('/', 1)[0]  # Directory URL
    headers = {"Authorization": f"token {github_pat}"}
    response = requests.get(directory_url, headers=headers)
    
    st.write("Debug: Checking directory existence at", directory_url)  # Debugging line
    st.write("Debug: Response status code", response.status_code)  # Debugging line

    if response.status_code == 404:
        st.warning("The `data` directory does not exist in the repository. Create it manually.")
        return False
    elif response.status_code != 200:
        st.error(f"Error checking directory existence: {response.status_code}")
        st.write("Debug: Response details", response.text)  # Debugging line
        return False
    st.success("Directory `data` exists in the repository.")
    return True

def load_existing_data():
    """Load existing data from the GitHub repository."""
    if not ensure_directory_exists():
        return []

    github_pat = get_github_pat()
    headers = {"Authorization": f"token {github_pat}"}
    response = requests.get(GITHUB_API_URL_JSON, headers=headers)
    
    if response.status_code == 200:
        content = response.json().get("content", "")
        if content:
            return json.loads(base64.b64decode(content).decode("utf-8"))
    elif response.status_code == 404:
        st.warning("No existing data found. A new file will be created.")
        return []
    else:
        st.error(f"Failed to load existing data. Error {response.status_code}: {response.text}")
        return []

def save_results_to_github(data):
    """Save results to the GitHub repository."""
    if not ensure_directory_exists():
        return

    github_pat = get_github_pat()
    if not github_pat:
        return

    existing_data = load_existing_data()
    existing_data.append(data)

    headers = {
        "Authorization": f"token {github_pat}",
        "Accept": "application/vnd.github.v3+json",
    }

    # Prepare payload
    encoded_content = base64.b64encode(json.dumps(existing_data, indent=4).encode("utf-8")).decode("utf-8")
    commit_message = "Update awareness.json with new responses"

    # Get the SHA of the existing file if it exists
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
        st.write("Debug: Response details", save_response.text)  # Debugging line

# Awareness Test
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
            "q9": 3
        }

    # Questions ...
    # (Include all test questions as in the original script)

    # Submit Test
    if st.button("Submit Test"):
        responses = st.session_state["awareness_responses"]
        score = 0
        # Calculate the score ...
        save_results_to_github({"score": score, "responses": responses})
        st.success("Your results have been saved successfully!")
