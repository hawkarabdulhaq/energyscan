import streamlit as st

def wellbeing_test():
    st.title("Well-Being and Balance Assessment")

    st.markdown("""
    **Evaluate your current state of work-life balance, physical and mental well-being, and overall recovery habits.**
    """)

    # Initialize score
    score = 0

    # Section 1: Work-Life Balance
    st.subheader("Section 1: Work-Life Balance")
    q1 = st.radio(
        "How often do you set boundaries between work and personal time?",
        [
            "A. Always, I maintain clear boundaries.",
            "B. Often, but I occasionally let them overlap.",
            "C. Rarely, work often spills into personal time.",
            "D. Never, I struggle to separate the two."
        ],
        key="wb_q1"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q1[0]]

    q2 = st.radio(
        "Do you allocate time for activities that rejuvenate you (e.g., hobbies, relaxation)?",
        [
            "A. Always, I make it a priority.",
            "B. Often, but not consistently.",
            "C. Rarely, I find it hard to make time.",
            "D. Never, I’m too busy to focus on myself."
        ],
        key="wb_q2"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q2[0]]

    # Section 2: Physical and Mental Well-Being
    st.subheader("Section 2: Physical and Mental Well-Being")
    q3 = st.radio(
        "How consistent are you in maintaining physical health (e.g., exercise, healthy diet)?",
        [
            "A. Very consistent, I prioritize my physical well-being.",
            "B. Fairly consistent, but I occasionally slip.",
            "C. Inconsistent, I struggle to maintain a routine.",
            "D. Not consistent at all."
        ],
        key="wb_q3"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q3[0]]

    q4 = st.radio(
        "How often do you take steps to manage stress (e.g., mindfulness, breaks, support)?",
        [
            "A. Always, I actively manage stress effectively.",
            "B. Often, but I could improve my strategies.",
            "C. Rarely, I manage stress reactively.",
            "D. Never, I feel overwhelmed most of the time."
        ],
        key="wb_q4"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q4[0]]

    # Section 3: Social and Emotional Health
    st.subheader("Section 3: Social and Emotional Health")
    q5 = st.radio(
        "Do you regularly spend quality time with family, friends, or a support system?",
        [
            "A. Always, I maintain strong relationships.",
            "B. Often, but I sometimes get too busy.",
            "C. Rarely, I feel disconnected at times.",
            "D. Never, I struggle to maintain connections."
        ],
        key="wb_q5"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q5[0]]

    q6 = st.radio(
        "How well do you handle emotional challenges or setbacks?",
        [
            "A. Very well, I address them constructively.",
            "B. Fairly well, but I sometimes need help.",
            "C. Rarely well, I often feel stuck.",
            "D. Not well at all, I feel overwhelmed."
        ],
        key="wb_q6"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q6[0]]

    # Section 4: Rest and Recovery
    st.subheader("Section 4: Rest and Recovery")
    q7 = st.radio(
        "Do you consistently prioritize adequate sleep and recovery time?",
        [
            "A. Always, I have a consistent sleep and recovery routine.",
            "B. Often, but I occasionally sacrifice rest for other tasks.",
            "C. Rarely, I prioritize other tasks over rest.",
            "D. Never, I frequently feel sleep-deprived and fatigued."
        ],
        key="wb_q7"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q7[0]]

    # Display Results
    if st.button("Submit Test"):
        st.subheader("Your Results")
        st.write(f"**Your Total Score: {score}**")
        if score >= 28:
            st.success("You are at the **Peak Balance** level. You excel at sustaining a healthy work-life balance!")
        elif score >= 20:
            st.info("You are at a **Moderate Balance** level. Consider fine-tuning routines to enhance well-being.")
        elif score >= 12:
            st.warning("You are at a **Low Balance** level. Focus on improving boundaries and routines.")
        else:
            st.error("You are at a **Very Low Balance** level. Prioritize self-care and rest to improve your well-being.")
