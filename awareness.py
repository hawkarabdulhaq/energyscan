import streamlit as st

def awareness_test():
    st.title("Energy Awareness Test")
    
    st.markdown("""
    **Answer the following questions to assess your energy performance level.**
    """)

    # Initialize score
    score = 0

    # Section 1: Awareness
    st.subheader("Section 1: Awareness")
    
    # Yes/No Question
    q1 = st.radio(
        "Do you feel you understand your natural energy highs and lows during the day?",
        ["Yes", "No"],
        key="awareness_q1"
    )
    score += 4 if q1 == "Yes" else 2

    # Likert Scale
    q2 = st.slider(
        "How well can you predict your peak energy times during the day?",
        min_value=1, max_value=5,
        value=3,
        format="Level %d",
        key="awareness_q2"
    )
    score += q2

    # Multiple-Choice
    q3 = st.radio(
        "How do you become aware of your energy levels?",
        [
            "A. Through regular tracking or journaling.",
            "B. Occasionally reflect on energy levels.",
            "C. Only notice during extreme highs/lows.",
            "D. Rarely think about energy levels."
        ],
        key="awareness_q3"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q3[0]]

    # Section 2: Task Alignment
    st.subheader("Section 2: Task Alignment")
    
    # Likert Scale
    q4 = st.slider(
        "How often do you schedule demanding tasks during your peak energy hours?",
        min_value=1, max_value=5,
        value=3,
        format="Level %d",
        key="alignment_q4"
    )
    score += q4

    # Checkbox for Multiple Selections
    q5 = st.multiselect(
        "What strategies do you use to handle tasks during low energy periods?",
        ["A. Adjust tasks to match energy levels.", "B. Take a short break or recharge.", 
         "C. Push through regardless.", "D. Delay tasks until later."],
        key="alignment_q5"
    )
    # Score based on chosen strategies
    strategy_scores = {"A. Adjust tasks to match energy levels.": 4, 
                       "B. Take a short break or recharge.": 3, 
                       "C. Push through regardless.": 2, 
                       "D. Delay tasks until later.": 1}
    for strategy in q5:
        score += strategy_scores[strategy]

    # Section 3: Consistency and Habits
    st.subheader("Section 3: Consistency and Habits")

    # Yes/No Question
    q6 = st.radio(
        "Do you maintain a consistent sleep schedule to optimize energy usage?",
        ["Yes", "No"],
        key="habits_q6"
    )
    score += 4 if q6 == "Yes" else 2

    # Likert Scale
    q7 = st.slider(
        "How consistent are you in taking regular breaks during work hours?",
        min_value=1, max_value=5,
        value=3,
        format="Level %d",
        key="habits_q7"
    )
    score += q7

    # Section 4: Self-Reflection
    st.subheader("Section 4: Self-Reflection")

    # Yes/No Question
    q8 = st.radio(
        "Do you feel in control of your energy usage daily?",
        ["Yes", "No"],
        key="reflection_q8"
    )
    score += 4 if q8 == "Yes" else 2

    # Likert Scale
    q9 = st.slider(
        "How satisfied are you with your current energy management?",
        min_value=1, max_value=5,
        value=3,
        format="Level %d",
        key="reflection_q9"
    )
    score += q9

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
