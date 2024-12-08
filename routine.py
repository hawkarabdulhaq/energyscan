import streamlit as st

def routine_test():
    st.title("Routine and Resilience Assessment")

    st.markdown("""
    **Evaluate your consistency, resilience, adaptability, and self-care habits to understand your ability to maintain and adapt routines.**
    """)

    # Initialize score
    score = 0

    # Section 1: Consistency
    st.subheader("Section 1: Consistency")
    q1 = st.radio(
        "How consistent are you in maintaining daily routines?",
        [
            "A. Extremely consistent, I rarely miss a day.",
            "B. Fairly consistent, but I occasionally skip.",
            "C. Inconsistent, I struggle to maintain routines.",
            "D. Not consistent at all."
        ],
        key="routine_q1"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q1[0]]

    q2 = st.radio(
        "How often do you review and adapt your habits based on changing circumstances?",
        [
            "A. Regularly, I reflect and adjust proactively.",
            "B. Occasionally, when I feel the need for improvement.",
            "C. Rarely, I resist changing routines.",
            "D. Never, I stick to the same habits regardless of outcomes."
        ],
        key="routine_q2"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q2[0]]

    # Section 2: Resilience Under Pressure
    st.subheader("Section 2: Resilience Under Pressure")
    q3 = st.radio(
        "When faced with unexpected challenges, how do you respond?",
        [
            "A. I adjust quickly and stay focused on my goals.",
            "B. I adapt eventually but feel stressed initially.",
            "C. I struggle to find my footing and often feel overwhelmed.",
            "D. I avoid addressing challenges and feel stuck."
        ],
        key="routine_q3"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q3[0]]

    q4 = st.radio(
        "How do you handle setbacks in your plans or goals?",
        [
            "A. I reflect, learn, and create new plans quickly.",
            "B. I recover eventually but dwell on the setback for some time.",
            "C. I find it difficult to recover and lose momentum.",
            "D. I often abandon goals after setbacks."
        ],
        key="routine_q4"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q4[0]]

    # Section 3: Growth and Learning
    st.subheader("Section 3: Growth and Learning")
    q5 = st.radio(
        "How actively do you seek opportunities for self-improvement and learning?",
        [
            "A. Very actively, I regularly challenge myself to grow.",
            "B. Fairly actively, I take opportunities as they come.",
            "C. Occasionally, but I often delay action.",
            "D. Rarely, I avoid stepping out of my comfort zone."
        ],
        key="routine_q5"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q5[0]]

    q6 = st.radio(
        "How adaptable are you when trying new strategies or techniques?",
        [
            "A. Very adaptable, I embrace changes quickly.",
            "B. Somewhat adaptable, but I hesitate at first.",
            "C. Rarely adaptable, I prefer sticking to familiar ways.",
            "D. Not adaptable, I resist trying new approaches."
        ],
        key="routine_q6"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q6[0]]

    # Section 4: Self-Care and Balance
    st.subheader("Section 4: Self-Care and Balance")
    q7 = st.radio(
        "How often do you prioritize self-care (e.g., rest, hobbies, mindfulness)?",
        [
            "A. Always, I balance work and self-care effectively.",
            "B. Often, but I neglect self-care during busy times.",
            "C. Rarely, I focus more on tasks than on self-care.",
            "D. Never, I view self-care as a low priority."
        ],
        key="routine_q7"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q7[0]]

    q8 = st.radio(
        "When your habits are disrupted, how do you regain balance?",
        [
            "A. Quickly, I have strategies to re-establish routines.",
            "B. Eventually, but it takes effort to get back on track.",
            "C. Slowly, I struggle to regain balance and consistency.",
            "D. I rarely regain balance and feel stuck."
        ],
        key="routine_q8"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q8[0]]

    # Display Results
    if st.button("Submit Test"):
        st.subheader("Your Results")
        st.write(f"**Your Total Score: {score}**")
        if score >= 28:
            st.success("You are at the **Peak Consistency and Resilience** level. You excel at maintaining and adapting routines effectively!")
        elif score >= 20:
            st.info("You are at a **Moderate Consistency and Resilience** level. Fine-tuning routines and resilience strategies will help you improve.")
        elif score >= 12:
            st.warning("You are at a **Low Consistency and Resilience** level. Focus on building stronger routines and adaptability.")
        else:
            st.error("You are at a **Very Low Consistency and Resilience** level. Prioritize strategies to regain balance and build resilience.")
