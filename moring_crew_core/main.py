import streamlit as st
from role import Role
from conversable_crew import ConversableCrew
from skillset import Skillset
from config.settings import DEFAULT_MODEL
from skillsets.internet_search import InternetSearch
from skillsets.twitter_search import TwitterSearch
from skillsets.meeting_notes_draft import MeetingNotesDraft
import asyncio

# Initialize skillsets
internet_skillset = InternetSearch(debug=True, answer_num=5)
twitter_search = TwitterSearch(debug=True, tweet_num=5)
meeting_notes_draft = MeetingNotesDraft(debug=True)

# Initialize roles
financial_researcher = Role(
    personal_info={
        "name": "Taylor Mason",
        "title": "Financial Researcher",
        "description": "Specializing in Social Media and Sentiment Analysis, A highly skilled financial research expert with a strong ability to gather and analyze information from diverse internet sources, including social media platforms like Twitter. Proficient in conducting social media sentiment analysis to assess market sentiment, trends, and public opinion on relevant financial topics. With expertise in leveraging advanced analytical frameworks, this professional integrates sentiment analysis into broader financial evaluations to provide accurate investment recommendations and risk control strategies. Their insights help identify potential opportunities and mitigate risks, ensuring well-informed decisions for investors and stakeholders."
    },
    skillsets=[internet_skillset, twitter_search]
)
analyst_intern = Role(
    personal_info={
        "name": "Ben Kim",
        "title": "Analyst Intern",
        "description": "Analyst Intern – Specializing in creating meeting notes and action plans. A dedicated Analyst Intern responsible for consolidating detailed meeting notes from the trading team, ensuring key takeaways are accurately captured and organized. Skilled in drafting comprehensive reports that summarize discussions and decisions made during trading crew meetings, this professional also creates and manages action plans to support the trading team’s execution of tasks and strategies. With strong attention to detail and excellent communication skills, they ensure that critical information is clearly conveyed and actionable, facilitating efficient follow-through on the team’s trading objectives."
    },
    skillsets=[meeting_notes_draft]
)

# Initialize ConversableCrew with the default model
crew = ConversableCrew([financial_researcher, analyst_intern], model_index=DEFAULT_MODEL)

# Streamlit UI
st.title("Conversational AI Chatbot")

if "conversation" not in st.session_state:
    st.session_state.conversation = []

def get_response(user_input):
    response = asyncio.run(crew.instruction(user_input))
    return response

user_input = st.text_input("Enter your instruction (or 'quit' to exit):")

if user_input:
    if user_input.lower() == 'quit':
        st.stop()
    else:
        response = get_response(user_input)
        st.session_state.conversation.append({"role": "user", "content": user_input})
        st.session_state.conversation.append({"role": "ai", "content": response})

if st.session_state.conversation:
    for entry in st.session_state.conversation:
        if entry["role"] == "user":
            st.write(f"**User:** {entry['content']}")
        else:
            st.write(f"**AI:** {entry['content']}")