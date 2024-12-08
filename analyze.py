import streamlit as st
from analyze_awareness import display_analysis as analyze_awareness

def display_analysis():
    st.title("📊 Analysis Dashboard")
    st.markdown("""
    **Welcome to the Analysis Section!**  
    This dashboard provides insights into your energy performance based on the surveys you've completed.  
    
    Explore the tabs below for detailed analyses of each survey:
    """)

    # Tabs for analysis
    tabs = st.tabs(["Awareness Analysis", "Routine Analysis (Coming Soon)", "Well-being Analysis (Coming Soon)", "Activities Analysis (Coming Soon)"])

    with tabs[0]:
        st.subheader("Awareness Analysis")
        analyze_awareness()

    with tabs[1]:
        st.subheader("Routine Analysis")
        st.info("Routine analysis is currently under development. Stay tuned!")

    with tabs[2]:
        st.subheader("Well-being Analysis")
        st.info("Well-being analysis is currently under development. Stay tuned!")

    with tabs[3]:
        st.subheader("Activities Analysis")
        st.info("Activities analysis is currently under development. Stay tuned!")
