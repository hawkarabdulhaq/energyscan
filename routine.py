import streamlit as st

def wellbeing_test():
    st.title("🌱 Well-being Test")
    st.markdown("""
    **Assess your balance between work, life, and self-care.**
    Answer questions to identify ways to improve physical and mental well-being.
    """)

    # Initialize score
    score = 0

    # Question 1
    st.subheader("1️⃣ Work-Life Balance")
    q1 = st.radio(
        "How often do you set boundaries between work and personal time?",
        ["A. Always, I maintain clear boundaries.",
         "B. Often, but I occasionally let them overlap.",
         "C. Rarely, work often spills into personal time.",
         "D. Never, I struggle to separate the two."],
        key="wellbeing_q1"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q1[0]]

    q2 = st.radio(
        "Do you allocate time for activities that rejuvenate you (e.g., hobbies, relaxation)?",
        ["A. Always, I make it a priority.",
         "B. Often, but not consistently.",
         "C. Rarely, I find it hard to make time.",
         "D. Never, I’m too busy to focus on myself."],
        key="wellbeing_q2"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q2[0]]

    # Question 2
    st.subheader("2️⃣ Physical and Mental Well-being")
    q3 = st.radio(
        "How consistent are you in maintaining physical health (e.g., exercise, healthy diet)?",
        ["A. Very consistent, I prioritize my physical well-being.",
         "B. Fairly consistent, but I occasionally slip.",
         "C. Inconsistent, I struggle to maintain a routine.",
         "D. Not consistent at all."],
        key="wellbeing_q3"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q3[0]]

    q4 = st.radio(
        "How often do you take steps to manage stress (e.g., mindfulness, breaks, support)?",
        ["A. Always, I actively manage stress effectively.",
         "B. Often, but I could improve my strategies.",
         "C. Rarely, I manage stress reactively.",
         "D. Never, I feel overwhelmed most of the time."],
        key="wellbeing_q4"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q4[0]]

    # Submit Button with Unique Key
    if st.button("Submit Test", key="wellbeing_submit"):
        st.subheader("Your Results")
        st.write(f"**Your Total Score: {score}**")
        if score >= 28:
            st.success("You're excelling at maintaining well-being!")
        elif 20 <= score < 28:
            st.info("You have good well-being practices but can improve further.")
        elif 12 <= score < 20:
            st.warning("Your well-being practices need work.")
        else:
            st.error("Consider focusing on improving your balance and self-care.")
