import streamlit as st
from survey import display_questionary
from analyze import display_analysis

# App Settings
APP_NAME = "Scan Your Energy Performance Lab"

def main():
    # Sidebar Header
    st.sidebar.title(APP_NAME)
    st.sidebar.markdown("---")
    
    # Sidebar Navigation with a persistent state
    page = st.sidebar.radio(
        "Navigate to:",
        ["🏠 Home", "📋 Survey", "📊 Analyze"],
        index=0 if st.session_state["current_page"] == "Home" else 1 if st.session_state["current_page"] == "Survey" else 2,
        key="navigation"
    )

    # Update session state based on selection
    if page == "🏠 Home":
        st.session_state["current_page"] = "Home"
    elif page == "📋 Survey":
        st.session_state["current_page"] = "Survey"
    elif page == "📊 Analyze":
        st.session_state["current_page"] = "Analyze"

    # Render the selected page
    if st.session_state["current_page"] == "Home":
        home_page()
    elif st.session_state["current_page"] == "Survey":
        display_questionary()
    elif st.session_state["current_page"] == "Analyze":
        display_analysis()

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
    
    👉 Use the sidebar to navigate to the Survey or Analysis sections and start your journey to optimizing energy performance!
    """)
    st.image("https://via.placeholder.com/800x200?text=Maximize+Your+Potential", use_column_width=True)

# Initialize Session State for Page Navigation
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Home"

if __name__ == "__main__":
    main()
