import streamlit as st
from survey import display_questionary
from analyze import display_analysis
from result import display_results

# App Settings
APP_NAME = "Scan Your Energy Performance Lab"

def main():
    # Sidebar Header
    st.sidebar.title(APP_NAME)
    st.sidebar.markdown("---")

    # Sidebar Buttons for Navigation
    if st.sidebar.button("🏠 Home"):
        st.session_state["current_page"] = "Home"
    if st.sidebar.button("📋 Survey"):
        st.session_state["current_page"] = "Survey"
    if st.sidebar.button("📊 Analyze"):
        st.session_state["current_page"] = "Analyze"
    if st.sidebar.button("📈 Results"):
        st.session_state["current_page"] = "Results"

    # Render the selected page
    if st.session_state["current_page"] == "Home":
        home_page()
    elif st.session_state["current_page"] == "Survey":
        display_questionary()
    elif st.session_state["current_page"] == "Analyze":
        display_analysis()
    elif st.session_state["current_page"] == "Results":
        display_results()

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
    
    👉 Use the sidebar to navigate to the Survey, Analysis, or Results sections and start your journey to optimizing energy performance!
    """)
    st.image("https://via.placeholder.com/800x200?text=Maximize+Your+Potential", use_container_width=True)

# Initialize Session State for Page Navigation
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Home"

if __name__ == "__main__":
    main()
