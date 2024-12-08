import streamlit as st
from survey import display_questionary

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
        display_questionary()

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

if __name__ == "__main__":
    main()
