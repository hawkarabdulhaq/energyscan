import streamlit as st

def routine_test():
    st.title("🛠️ Routine Test")
    st.markdown("""
    **Evaluate your consistency, resilience, adaptability, and self-care in daily routines.**
    """)
    
    # Initialize score
    score = 0

    # Question 1
    st.subheader("1️⃣ Consistency in Habits")
    q1 = st.radio(
        "How consistent are you in maintaining daily routines?",
        ["A. Extremely consistent, I rarely miss a day.",
         "B. Fairly consistent, but I occasionally skip.",
         "C. Inconsistent, I struggle to maintain routines.",
         "D. Not consistent at all."],
        key="routine_q1"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q1[0]]

    # Question 2
    q2 = st.radio(
        "How often do you review and adapt your habits based on changing circumstances?",
        ["A. Regularly, I reflect and adjust proactively.",
         "B. Occasionally, when I feel the need for improvement.",
         "C. Rarely, I resist changing routines.",
         "D. Never, I stick to the same habits regardless of outcomes."],
        key="routine_q2"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q2[0]]

    # Question 3
    st.subheader("2️⃣ Resilience Under Pressure")
    q3 = st.radio(
        "When faced with unexpected challenges, how do you respond?",
        ["A. I adjust quickly and stay focused on my goals.",
         "B. I adapt eventually but feel stressed initially.",
         "C. I struggle to find my footing and often feel overwhelmed.",
         "D. I avoid addressing challenges and feel stuck."],
        key="routine_q3"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q3[0]]

    # Question 4
    q4 = st.radio(
        "How do you handle setbacks in your plans or goals?",
        ["A. I reflect, learn, and create new plans quickly.",
         "B. I recover eventually but dwell on the setback for some time.",
         "C. I find it difficult to recover and lose momentum.",
         "D. I often abandon goals after setbacks."],
        key="routine_q4"
    )
    score += {"A": 4, "B": 3, "C": 2, "D": 1}[q4[0]]

    # Submit Button with Unique Key
    if st.button("Submit Test", key="routine_submit"):
        st.subheader("Your Results")
        st.write(f"**Your Total Score: {score}**")
        if score >= 28:
            st.success("You're highly resilient and consistent!")
        elif 20 <= score < 28:
            st.info("You have a good level of consistency but can improve.")
        elif 12 <= score < 20:
            st.warning("Your consistency and resilience need work.")
        else:
            st.error("Consider building better routines and resilience strategies.")
