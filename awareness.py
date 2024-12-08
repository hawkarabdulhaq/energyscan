import streamlit as st
import json
import os

def save_results_to_file(data, file_path="data/awareness.json"):
    """Save results to a JSON file."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            existing_data = json.load(file)
    else:
        existing_data = []
    
    existing_data.append(data)
    with open(file_path, "w") as file:
        json.dump(existing_data, file, indent=4)

def awareness_test():
    st.title("Energy Awareness Test")
    st.markdown("**Answer the following questions to assess your energy performance level.**")

    # Initialize score
    score = 0

    # Session state for responses
    if "responses" not in st.session_state:
        st.session_state["responses"] = {
            "awareness_q1": None,
            "awareness_q2": None,
            "awareness_q3": None,
            "alignment_q4": None,
            "alignment_q5": [],
            "habits_q6": None,
            "habits_q7": None,
            "reflection_q8": None,
            "reflection_q9": None
        }

    # Section 1: Awareness
    st.subheader("Section 1: Awareness")
    st.session_state["responses"]["awareness_q1"] = st.radio(
        "Do you feel you understand your natural energy highs and lows during the day?",
        ["Yes", "No"],
        index=0 if st.session_state["responses"]["awareness_q1"] == "Yes" else 1,
        key="awareness_q1"
    )
    score += 4 if st.session_state["responses"]["awareness_q1"] == "Yes" else 2

    st.session_state["responses"]["awareness_q2"] = st.slider(
        "How well can you predict your peak energy times during the day?",
        min_value=1, max_value=5,
        value=st.session_state["responses"]["awareness_q2"] or 3,
        format="Level %d",
        key="awareness_q2"
    )
    score += st.session_state["responses"]["awareness_q2"]

    st.session_state["responses"]["awareness_q3"] = st.radio(
        "How do you become aware of your energy levels?",
        [
            "A. Through regular tracking or journaling.",
            "B. Occasionally reflect on energy levels.",
            "C. Only notice during extreme highs/lows.",
            "D. Rarely think about energy levels."
        ],
        index={
            "A": 0, "B": 1, "C": 2, "D": 3
        }[st.session_state["responses"]["awareness_q3"][0]] if st.session_state["responses"]["awareness_q3"] else 0,
        key="awareness_q3"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[st.session_state["responses"]["awareness_q3"][0]]

    # Section 2: Task Alignment
    st.subheader("Section 2: Task Alignment")
    st.session_state["responses"]["alignment_q4"] = st.slider(
        "How often do you schedule demanding tasks during your peak energy hours?",
        min_value=1, max_value=5,
        value=st.session_state["responses"]["alignment_q4"] or 3,
        format="Level %d",
        key="alignment_q4"
    )
    score += st.session_state["responses"]["alignment_q4"]

    st.session_state["responses"]["alignment_q5"] = st.multiselect(
        "What strategies do you use to handle tasks during low energy periods?",
        ["A. Adjust tasks to match energy levels.", "B. Take a short break or recharge.", 
         "C. Push through regardless.", "D. Delay tasks until later."],
        default=st.session_state["responses"]["alignment_q5"],
        key="alignment_q5"
    )
    strategy_scores = {"A. Adjust tasks to match energy levels.": 4, 
                       "B. Take a short break or recharge.": 3, 
                       "C. Push through regardless.": 2, 
                       "D. Delay tasks until later.": 1}
    score += sum(strategy_scores[strategy] for strategy in st.session_state["responses"]["alignment_q5"])

    # Section 3: Consistency and Habits
    st.subheader("Section 3: Consistency and Habits")
    st.session_state["responses"]["habits_q6"] = st.radio(
        "Do you maintain a consistent sleep schedule to optimize energy usage?",
        ["Yes", "No"],
        index=0 if st.session_state["responses"]["habits_q6"] == "Yes" else 1,
        key="habits_q6"
    )
    score += 4 if st.session_state["responses"]["habits_q6"] == "Yes" else 2

    st.session_state["responses"]["habits_q7"] = st.slider(
        "How consistent are you in taking regular breaks during work hours?",
        min_value=1, max_value=5,
        value=st.session_state["responses"]["habits_q7"] or 3,
        format="Level %d",
        key="habits_q7"
    )
    score += st.session_state["responses"]["habits_q7"]

    # Section 4: Self-Reflection
    st.subheader("Section 4: Self-Reflection")
    st.session_state["responses"]["reflection_q8"] = st.radio(
        "Do you feel in control of your energy usage daily?",
        ["Yes", "No"],
        index=0 if st.session_state["responses"]["reflection_q8"] == "Yes" else 1,
        key="reflection_q8"
    )
    score += 4 if st.session_state["responses"]["reflection_q8"] == "Yes" else 2

    st.session_state["responses"]["reflection_q9"] = st.slider(
        "How satisfied are you with your current energy management?",
        min_value=1, max_value=5,
        value=st.session_state["responses"]["reflection_q9"] or 3,
        format="Level %d",
        key="reflection_q9"
    )
    score += st.session_state["responses"]["reflection_q9"]

    # Submit Test
    if st.button("Submit Test"):
        st.subheader("Your Results")
        st.write(f"**Your Total Score: {score}**")
        if score >= 36:
            st.success("You are at the **Peak Performance** level. Keep up the excellent energy management!")
        elif 24 <= score < 36:
            st.info("You are at a **Moderate Performance** level. Focus on consistency to improve further.")
        elif 12 <= score < 24:
            st.warning("You are at a **Low Performance** level. Consider building better routines and tracking energy.")
        else:
            st.error("You are at a **Very Low Performance** level. Let's work on understanding your energy patterns.")

        # Save Results
        user_data = {"score": score, "responses": st.session_state["responses"]}
        save_results_to_file(user_data)
        st.success("Your results have been saved successfully!")
