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
    I can diagnose your energy level by asking you the questions below. Your task is to carefully engage with my questions, and I will tell you what your performance level is.
    """)
    
    # User Details Form
    st.subheader("📝 Please provide your details to get started:")
    with st.form("user_details_form"):
        name = st.text_input("Your Name")
        age = st.number_input("Your Age", min_value=1, max_value=120, step=1)
        gender = st.radio("Your Gender", ["Male", "Female", "Other"])
        
        # Submit Button
        start_test = st.form_submit_button("Start Test")
    
    if start_test:
        if name and age:
            st.success(f"Hello {name}! You are ready to start the test. 🚀")
            st.write("Use the sidebar to navigate to the Questionary and get started.")
        else:
            st.error("Please fill in all the fields to proceed.")

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
