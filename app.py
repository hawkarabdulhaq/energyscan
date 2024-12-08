import streamlit as st

def main():
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
            st.write("Get ready to engage with the questions in the next step!")
        else:
            st.error("Please fill in all the fields to proceed.")

if __name__ == "__main__":
    main()
