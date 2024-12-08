import streamlit as st
from awareness import awareness_test
from routine import routine_test
from wellbeing import wellbeing_test
from activities import activities_test

def main():
    # Sidebar Navigation
    st.sidebar.title("Navigation")
    menu = st.sidebar.radio(
        "Choose a Section",
        ["Home", "Questionary"]
    )
    
    if menu == "Home":
        home_page()
    elif menu == "Questionary":
        questionary_page()

def home_page():
    # App Title
    st.title("Welcome to Scan Your Energy Performance Lab")
    
    # App Description
    st.markdown("""
    🌟 **Discover Your Energy Performance**  
    This test is designed to help you understand your energy patterns and performance levels.  
    By answering carefully curated questions, you'll gain insights into:  
    - How effectively you manage your energy.  
    - Areas for improvement in your daily routines and habits.  
    - Steps to enhance your productivity and well-being.  
    
    👉 Use the sidebar to navigate to the Questionary and start the journey to understanding your energy better!
    """)

def questionary_page():
    st.title("📋 Questionary Sections")
    
    # Section Selection
    section = st.radio(
        "Choose a section to perform the questionary:",
        ["Awareness", "Routine", "Well-being", "Activities"]
    )
    
    if section == "Awareness":
        st.header("Awareness Questionary")
        awareness_test()
    elif section == "Routine":
        st.header("Routine Questionary")
        routine_test()
    elif section == "Well-being":
        st.header("Well-being Questionary")
        wellbeing_test()
    elif section == "Activities":
        st.header("Activities Questionary")
        activities_test()

if __name__ == "__main__":
    main()
