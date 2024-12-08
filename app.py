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

    # Sidebar Navigation with Buttons
    if st.sidebar.button("🏠 Home"):
        st.session_state["current_page"] = "Home"
    if st.sidebar.button("📋 Survey"):
        st.session_state["current_page"] = "Survey"
    if st.sidebar.button("📊 Analyze"):
        st.session_state["current_page"] = "Analyze"
    if st.sidebar.button("📈 Results"):
        st.session_state["current_page"] = "Results"

    # Sidebar Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Course by Hawkar Ali Abdulhaq")
    st.sidebar.markdown("🌐 [www.habdulhaq.com](https://www.habdulhaq.com)")
    st.sidebar.markdown("📧 [connect@habdulhaq.com](mailto:connect@habdulhaq.com)")
    
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
    st.markdown("---")
    st.markdown("**Course by Hawkar Ali Abdulhaq**")
    st.markdown("🌐 [www.habdulhaq.com](https://www.habdulhaq.com)")
    st.markdown("📧 [connect@habdulhaq.com](mailto:connect@habdulhaq.com)")

    # Display personal image
    try:
        st.image("data/personal.jpg", use_container_width=True, caption="Scan Your Energy Performance Lab")
    except FileNotFoundError:
        st.warning("Image not found. Please ensure `data/personal.jpg` exists.")

# Initialize Session State for Page Navigation
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Home"

if __name__ == "__main__":
    main()
