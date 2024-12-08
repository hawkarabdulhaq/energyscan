def display_routine_analysis():
    st.title("📊 Routine Analysis")
    st.markdown("""
    **Evaluate Your Routine Management**  
    This section analyzes your responses to the Routine Survey to identify strengths and areas for improvement.
    """)

    # Load data
    data = load_existing_data()
    if not data:
        st.warning("No data available for analysis.")
        return

    # Select a specific response to analyze
    st.markdown("### Select a Response to Analyze")
    selected_index = st.selectbox(
        "Choose a response:",
        options=list(range(len(data))),
        format_func=lambda i: f"Response {i + 1}",
        key="routine_response_selector"  # Added a unique key
    )
    selected_response = data[selected_index]["responses"]

    # Display classification
    classification, total_score = classify_routine(selected_response)
    st.subheader("📋 Classification Results")
    st.info(f"**Classification:** {classification}")
    st.metric("Total Score", f"{total_score}/40")

    # Visualization of Score Distribution
    st.markdown("### 📊 Score Distribution")
    score_categories = ["Consistency", "Adaptability", "Self-Care", "Reflection"]
    scores = [
        selected_response["q2"],
        selected_response["q3"],
        selected_response["q6"],
        4 if selected_response["q7"] == "Yes" else 2
    ]
    fig = px.bar(x=score_categories, y=scores, labels={"x": "Category", "y": "Score"}, title="Score Distribution")
    st.plotly_chart(fig, use_container_width=True)

    # Display analysis
    st.subheader("📋 Analysis Results")
    good, improvement = analyze_responses(selected_response)

    # Strengths
    st.markdown("#### ✅ What is Good")
    if good:
        for item in good:
            st.write(f"- {item}")
    else:
        st.write("No significant strengths identified.")

    # Areas for Improvement
    st.markdown("#### 🔍 What Needs Improvement")
    if improvement:
        for item in improvement:
            st.write(f"- {item}")
    else:
        st.success("No significant areas for improvement were identified.")
