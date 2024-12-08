import streamlit as st

def activities_test():
    st.title("Task Prioritization and Activity Impact Test")

    st.markdown("""
    **Answer the following questions to evaluate your ability to prioritize tasks and focus on high-impact activities.**
    """)

    # Initialize score
    score = 0

    # Section 1: Task Prioritization
    st.subheader("Section 1: Task Prioritization")
    q1 = st.radio(
        "How often do you prioritize tasks based on their impact rather than urgency?",
        [
            "A. Always, I focus on high-impact tasks first.",
            "B. Often, but I sometimes get distracted by urgent tasks.",
            "C. Rarely, I work on tasks as they come.",
            "D. Never, I struggle to prioritize effectively."
        ],
        key="q1"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q1[0]]

    q2 = st.radio(
        "Do you regularly identify which tasks are most critical to your goals?",
        [
            "A. Yes, I have a clear list of critical tasks.",
            "B. Sometimes, but I need reminders or reviews.",
            "C. Rarely, I lack a clear understanding of what’s critical.",
            "D. Never, I treat all tasks equally."
        ],
        key="q2"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q2[0]]

    # Section 2: Clarity of Goals
    st.subheader("Section 2: Clarity of Goals")
    q3 = st.radio(
        "How clear are your goals for each day or week?",
        [
            "A. Very clear, I know exactly what I need to achieve.",
            "B. Somewhat clear, but I revisit them frequently.",
            "C. Rarely clear, I often feel unsure of my objectives.",
            "D. Not clear at all, I work without specific goals."
        ],
        key="q3"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q3[0]]

    q4 = st.radio(
        "Do you break down larger goals into smaller, manageable tasks?",
        [
            "A. Always, I consistently use task breakdowns.",
            "B. Often, but I occasionally skip this step.",
            "C. Rarely, I struggle to break down large goals.",
            "D. Never, I work without planning steps."
        ],
        key="q4"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q4[0]]

    # Section 3: Awareness of Impact
    st.subheader("Section 3: Awareness of Impact")
    q5 = st.radio(
        "How well do you evaluate the potential impact of tasks before starting them?",
        [
            "A. Very well, I consider the outcome of each task.",
            "B. Often, but I sometimes act without thinking it through.",
            "C. Rarely, I don’t evaluate impact effectively.",
            "D. Never, I complete tasks without assessing their value."
        ],
        key="q5"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q5[0]]

    q6 = st.radio(
        "How often do you delegate or avoid low-impact activities?",
        [
            "A. Always, I focus only on tasks that add value.",
            "B. Often, but I occasionally handle low-impact tasks myself.",
            "C. Rarely, I find it difficult to delegate or avoid tasks.",
            "D. Never, I handle all tasks regardless of impact."
        ],
        key="q6"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q6[0]]

    # Section 4: Productivity and Focus
    st.subheader("Section 4: Productivity and Focus")
    q7 = st.radio(
        "How focused are you when working on high-impact tasks?",
        [
            "A. Fully focused, I eliminate distractions.",
            "B. Mostly focused, but I sometimes get distracted.",
            "C. Rarely focused, I struggle to maintain concentration.",
            "D. Not focused at all, I find it hard to concentrate."
        ],
        key="q7"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q7[0]]

    q8 = st.radio(
        "How often do you reflect on whether your efforts are aligned with your long-term goals?",
        [
            "A. Regularly, I consistently evaluate my progress.",
            "B. Sometimes, but I need reminders to reflect.",
            "C. Rarely, I don’t reflect on my goals.",
            "D. Never, I work without alignment to goals."
        ],
        key="q8"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q8[0]]

    # Display Results
    if st.button("Submit Test"):
        st.subheader("Your Results")
        st.write(f"**Your Total Score: {score}**")
        if score >= 28:
            st.success("You are at the **Optimal Prioritization** level. You excel at focusing on high-impact tasks!")
        elif score >= 20:
            st.info("You are at a **Moderate Prioritization** level. Consider refining your focus for better impact.")
        elif score >= 12:
            st.warning("You are at a **Low Prioritization** level. Work on clarity and task alignment.")
        else:
            st.error("You are at a **Very Low Prioritization** level. Start by identifying critical tasks and goals.")
