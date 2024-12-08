import streamlit as st
from awareness import awareness_test
from routine import routine_test
from wellbeing import wellbeing_test
from activities import activities_test

def display_questionary():
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
