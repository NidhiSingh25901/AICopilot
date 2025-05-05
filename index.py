import streamlit as st
from ai_assistant import get_ai_response

st.set_page_config(layout="wide")
st.title("🧠 AI Copilot: Innovation Challenge Builder")

# Initialize session state
if "challenge_data" not in st.session_state:
    st.session_state.challenge_data = {}

# Define a simple knowledge base
knowledge_base = {
    "What is an innovation challenge?": "An innovation challenge is a competition where participants solve specific problems or create new ideas.",
    "How do I define a challenge?": "You can define a challenge by specifying its title, problem statement, goals, and type.",
    "What are the types of challenges?": "Common types include Ideation, Development, Data Science, and AI challenges.",
    "How can I set the audience for my challenge?": "You can set the audience by specifying whether it's open to the public or invite-only, and defining allowed geographies and languages."
}

# Sidebar Chat Assistant
with st.sidebar:
    st.header("💬 Copilot Assistant")
    user_input = st.text_input("Ask me anything", key="chat_input")
    if st.button("Ask"):
        if user_input:
            with st.spinner("Thinking..."):
                # Maintain conversation history for multi-turn conversations
                context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.get("conversation_history", [])])
                response = get_ai_response(user_input, context=context)
                
                # Save conversation history
                if "conversation_history" not in st.session_state:
                    st.session_state.conversation_history = []
                st.session_state.conversation_history.append({"role": "user", "content": user_input})
                st.session_state.conversation_history.append({"role": "assistant", "content": response})
                
                st.markdown(f"**AI Copilot:** {response}")
        else:
            st.info("Enter a question to ask the AI copilot.")

# Define Tabs
tabs = st.tabs([
    "1. Define Challenge",
    "2. Set Audience",
    "3. Submission Requirements",
    "4. Configure Prizes",
    "5. Timeline & Milestones",
    "6. Evaluation Criteria",
    "7. Monitor Challenge",
])

# --- STEP 1: Define Your Challenge ---
with tabs[0]:
    st.subheader("📝 Define Your Challenge")
    title = st.text_input("Challenge Title", help="Example: 'AI for Good: Predicting Climate Change Impact'")
    problem = st.text_area("Problem Statement", help="Describe the problem you want to solve.")
    goals = st.multiselect("Challenge Goals", ["Business", "Technical", "Social"], help="Select one or more goals for your challenge.")
    challenge_type = st.selectbox("Challenge Type", ["Ideation", "Development", "Data Science", "AI"], help="Choose the type of challenge.")

    if st.button("Suggest Better Problem Statement"):
        if problem:
            prompt = f"Improve and clarify this problem statement for an innovation challenge: {problem}"
            improved = get_ai_response(prompt)
            st.text_area("✨ Suggested by AI", improved, height=150)
        else:
            st.warning("Please enter a problem statement first.")

    # Validate inputs
    if not title:
        st.warning("Challenge title is required.")
    if len(problem) < 50:
        st.warning("Problem statement should be at least 50 characters long.")

    st.session_state.challenge_data['define'] = {
        "title": title, "problem": problem,
        "goals": goals, "type": challenge_type
    }

    # Request support button
    if st.button("📞 Request Support"):
        st.info("A platform representative will contact you shortly.")

# --- STEP 2: Audience & Registration ---
with tabs[1]:
    st.subheader("👥 Set Your Audience")
    audience = st.radio("Who can join?", ["Open to Public", "Invite Only"], help="Select the audience type.")
    
    if audience == "Open to Public":
        geography = st.text_input("Allowed Geographies (e.g., Global, US-only)", help="Specify the geographical restrictions.")
        language = st.selectbox("Primary Language", ["English", "Spanish", "French"], help="Select the primary language for the challenge.")
    else:
        st.info("Since this is an invite-only challenge, public audience settings are skipped.")
        geography, language = None, None

    teams = st.checkbox("Allow Team Participation?", help="Enable team participation for the challenge.")
    forums = st.checkbox("Enable Forums / Q&A Boards?", help="Allow participants to interact via forums or Q&A boards.")

    st.session_state.challenge_data['audience'] = {
        "type": audience,
        "geography": geography,
        "language": language,
        "teams": teams,
        "forums": forums
    }

    # Request support button
    if st.button("📞 Request Support", key="audience_support"):
        st.info("A platform representative will contact you shortly.")

# --- Continue for other tabs similarly ---
with tabs[2]:
    st.subheader("📦 Submission Requirements")
    formats = st.multiselect("Accepted Submission Formats", ["ZIP", "GitHub Repo", "Google Drive Link"])
    documents = st.multiselect("Required Docs", ["README", "Demo Video", "Architecture Diagram"])

    st.session_state.challenge_data['submission'] = {
        "formats": formats,
        "documents": documents
    }

with tabs[3]:
    st.subheader("🏆 Configure Prizes")
    model = st.radio("Prize Model", ["Single Winner", "Tiered", "Milestone-based"])
    budget = st.number_input("Total Prize Budget ($)", min_value=0)
    if st.button("AI Suggest Prize Breakdown"):
        suggestion_prompt = f"Suggest a prize distribution model for a {model} format with a ${budget} budget."
        prize_suggestion = get_ai_response(suggestion_prompt)
        st.markdown(f"**Suggested by AI:**\n{prize_suggestion}")

    st.session_state.challenge_data['prizes'] = {
        "model": model,
        "budget": budget
    }

with tabs[4]:
    st.subheader("⏳ Timeline & Milestones")
    start = st.date_input("Challenge Start Date")
    end = st.date_input("Challenge End Date")
    registration = st.date_input("Registration Deadline")
    prototype = st.date_input("Prototype Review Date")

    st.session_state.challenge_data['timeline'] = {
        "start": start,
        "end": end,
        "registration": registration,
        "prototype": prototype
    }

with tabs[5]:
    st.subheader("🧪 Evaluation Criteria")
    eval_model = st.radio("Evaluation Model", ["Rolling", "Post-Submission"])
    reviewers = st.multiselect("Assign Reviewers", ["Internal", "External", "AI-assisted"])
    scoring = st.text_area("Describe Scoring Criteria")
    if st.button("AI Generate Rubric"):
        rubric_prompt = f"Generate a review rubric for: {scoring}"
        rubric = get_ai_response(rubric_prompt)
        st.markdown(f"**AI-Generated Rubric:**\n{rubric}")

    st.session_state.challenge_data['evaluation'] = {
        "model": eval_model,
        "reviewers": reviewers,
        "criteria": scoring
    }

with tabs[6]:
    st.subheader("📡 Monitor Your Challenge")
    alerts = st.multiselect("Set up Notifications", ["Email", "In-App", "Slack"])
    st.session_state.challenge_data['monitor'] = {"alerts": alerts}
    st.success("✅ Challenge creation steps saved in session.")

# Final Actions
st.markdown("---")
if st.button("🚀 Submit & Launch Challenge"):
    st.success("🎉 Your challenge has been launched!")
    st.json(st.session_state.challenge_data)

if st.button("📞 Request Human Support"):
    st.info("A platform representative will contact you shortly.")

# Feedback Form
st.markdown("---")
st.header("📋 Feedback Form")
st.text_area("What did you like about the onboarding experience?", key="feedback_positive")
st.text_area("What can we improve?", key="feedback_negative")
if st.button("Submit Feedback"):
    feedback = {
        "positive": st.session_state.get("feedback_positive", ""),
        "negative": st.session_state.get("feedback_negative", "")
    }
    st.success("Thank you for your feedback!")
    # Save feedback (e.g., to a file or database)
    with open("feedback.json", "a") as f:
        import json
        json.dump(feedback, f)
        f.write("\n")