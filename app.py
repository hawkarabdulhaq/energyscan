import streamlit as st
from survey import display_questionary

def main():
    # App Configuration
    st.set_page_config(
        page_title="Energy Performance Lab",
        page_icon="⚡",
        layout="wide",
    )
    
    # Sidebar Navigation
    st.sidebar.title("⚡ Energy Performance Lab")
    st.sidebar.markdown("---")
    
    st.sidebar.subheader("Navigation")
    if st.sidebar.button("🏠 Home"):
        home_page()
    if st.sidebar.button("📋 Awareness"):
        display_questionary(section="Awareness")
    if st.sidebar.button("📋 Routine"):
        display_questionary(section="Routine")
    if st.sidebar.button("📋 Well-being"):
        display_questionary(section="Well-being")
    if st.sidebar.button("📋 Activities"):
        display_questionary(section="Activities")
    
    st.sidebar.markdown("---")
    st.sidebar.write("✨ Discover your energy potential!")

def home_page():
    # Home Page Content
    st.title("Welcome to Scan Your Energy Performance Lab")
    st.markdown("""
    🌟 **Discover Your Energy Performance**  
    Unlock insights into your energy management and performance levels with our personalized questionary.  
    - **Awareness**: Understand your peak energy times and patterns.  
    - **Routine**: Build effective, resilient routines.  
    - **Well-being**: Achieve balance in life and work.  
    - **Activities**: Prioritize tasks for maximum impact.  
    
    🖱️ Use the buttons in the sidebar to explore each section of the questionary and start your journey!
    """)

if __name__ == "__main__":
    main()
