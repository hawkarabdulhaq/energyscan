import streamlit as st
from analyze_awareness import display_analysis as analyze_awareness
from analyze_routine import display_routine_analysis as analyze_routine
from analyze_wellbeing import display_wellbeing_analysis as analyze_wellbeing
from analyze_activities import display_activities_analysis as analyze_activities


def display_analysis():
    st.title("📊 Analysis Dashboard")
    st.markdown("""
    **Welcome to the Analysis Section!**  
    This dashboard provides insights into your energy performance based on the surveys you've completed.  
    Use the tabs below to explore detailed analyses for each survey.
    """)

    # Tabs for analysis
    tabs = st.tabs([
        "Awareness Analysis",
        "Routine Analysis",
        "Well-being Analysis",
        "Activities Analysis"
    ])

    with tabs[0]:
        st.subheader("Awareness Analysis")
        analyze_awareness()

    with tabs[1]:
        st.subheader("Routine Analysis")
        analyze_routine()

    with tabs[2]:
        st.subheader("Well-being Analysis")
        analyze_wellbeing()

    with tabs[3]:
        st.subheader("Activities Analysis")
        analyze_activities()
