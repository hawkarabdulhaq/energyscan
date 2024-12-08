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
    q1 = st.radio(
        "How aware are you of your peak energy times during the day?",
        ["A. Very aware and can identify them easily.",
         "B. Somewhat aware, but I need reminders.",
         "C. Rarely aware and often guess.",
         "D. Not aware at all."],
        key="q1"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q1[0]]

    q2 = st.radio(
        "Do you track your energy levels throughout the day?",
        ["A. Yes, I track them regularly (e.g., journaling, app).",
         "B. Occasionally, but not consistently.",
         "C. Rarely, only when I feel extreme highs or lows.",
         "D. Never."],
        key="q2"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q2[0]]

    # Section 2: Task Alignment
    st.subheader("Section 2: Task Alignment")
    q3 = st.radio(
        "How often do you align demanding tasks with your high-energy periods?",
        ["A. Always, I plan my work around these times.",
         "B. Often, but I sometimes miss opportunities.",
         "C. Rarely, I work without considering energy levels.",
         "D. Never, I complete tasks as they come."],
        key="q3"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q3[0]]

    q4 = st.radio(
        "When faced with a dip in energy, how do you handle tasks?",
        ["A. I adjust and focus on low-energy tasks.",
         "B. I push through but feel less productive.",
         "C. I struggle to complete anything.",
         "D. I give up or procrastinate."],
        key="q4"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q4[0]]

    # Section 3: Consistency and Habits
    st.subheader("Section 3: Consistency and Habits")
    q5 = st.radio(
        "How consistent are you in maintaining routines that optimize energy usage (e.g., sleep, breaks, nutrition)?",
        ["A. Very consistent, I have a structured routine.",
         "B. Fairly consistent, but I slip occasionally.",
         "C. Inconsistent, I struggle to maintain routines.",
         "D. Not consistent at all."],
        key="q5"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q5[0]]

    q6 = st.radio(
        "Do you take regular breaks to recharge during long work periods?",
        ["A. Always, I schedule breaks intentionally.",
         "B. Often, but I sometimes forget.",
         "C. Rarely, I feel guilty taking breaks.",
         "D. Never, I work until I'm drained."],
        key="q6"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q6[0]]

    # Section 4: Self-Reflection
    st.subheader("Section 4: Self-Reflection")
    q7 = st.radio(
        "How do you feel about your ability to manage energy effectively?",
        ["A. Confident, I feel in control of my energy usage.",
         "B. Positive, but I know I can improve.",
         "C. Uncertain, I often feel inefficient.",
         "D. Negative, I feel drained most of the time."],
        key="q7"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q7[0]]

    # Display Results
    if st.button("Submit Test"):
        st.subheader("Your Results")
        st.write(f"**Your Total Score: {score}**")
        if score >= 24:
            st.success("You are at the **Peak Performance** level. Keep up the excellent energy management!")
        elif score >= 16:
            st.info("You are at a **Moderate Performance** level. Focus on consistency to improve further.")
        elif score >= 8:
            st.warning("You are at a **Low Performance** level. Consider building better routines and tracking energy.")
        else:
            st.error("You are at a **Very Low Performance** level. Let's work on understanding your energy patterns.")

