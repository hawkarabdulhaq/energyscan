import streamlit as st
from awareness import awareness_test
from routine import routine_test
from wellbeing import wellbeing_test
from activities import activities_test

def display_questionary():
    st.title("📋 Questionary Sections")
    st.markdown(
        """
        Welcome to the Questionary!  
        Explore the four key areas of energy performance by expanding the sections below.  
        Each section contains specific questions to help you evaluate and enhance your energy management.
        """
    )
    # Tabs for each section
    with st.expander("1️⃣ Awareness"):
        st.subheader("Awareness Questionary")
        st.markdown("""
        **Discover how aware you are of your energy levels throughout the day.**  
        Answer questions to understand your energy patterns and habits.
        """)
        awareness_test()

    with st.expander("2️⃣ Routine"):
        st.subheader("Routine Questionary")
        st.markdown("""
        **Evaluate your consistency and adaptability in daily routines.**  
        Answer questions to uncover how structured and resilient your routines are.
        """)
        routine_test()

    with st.expander("3️⃣ Well-being"):
        st.subheader("Well-being Questionary")
        st.markdown("""
        **Assess your balance between work, life, and self-care.**  
        Answer questions to identify ways to improve physical and mental well-being.
        """)
        wellbeing_test()

    with st.expander("4️⃣ Activities"):
        st.subheader("Activities Questionary")
        st.markdown("""
        **Focus on prioritizing tasks and understanding their impact.**  
        Answer questions to optimize your efforts and productivity.
        """)
        activities_test()
