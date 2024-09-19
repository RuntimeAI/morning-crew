import streamlit as st
from role import Role
from conversable_crew import ConversableCrew
from skillset import Skillset
from config.settings import DEFAULT_MODEL
from skillsets.internet_search import InternetSearch
from skillsets.twitter_search import TwitterSearch
from skillsets.meeting_notes_draft import MeetingNotesDraft
import asyncio
from streamlit_chat import message  # Import streamlit_chat

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

def on_input_change():
    user_input = st.session_state.user_input
    if user_input.lower() == 'quit':
        st.stop()
    else:
        response = get_response(user_input)
        st.session_state.conversation.append({"role": "user", "content": user_input})
        st.session_state.conversation.append({"role": "ai", "content": response})
    st.session_state.user_input = ""

def on_btn_click():
    st.session_state.conversation = []

# Create a container for the chat history
chat_placeholder = st.container()

# Create a container at the bottom for the input box
input_placeholder = st.empty()

# Display the chat history in the chat_placeholder container
with chat_placeholder:
    chat_container = st.container()
    with chat_container:
        for entry in st.session_state.conversation:
            if entry["role"] == "user":
                message(entry['content'], is_user=True)
            else:
                message(entry['content'])
        st.button("Clear message", on_click=on_btn_click)

# Display the input box in the input_placeholder container
with input_placeholder:
    st.text_input("User Input:", on_change=on_input_change, key="user_input")

# Add custom CSS to center the containers, fix the input box at the bottom with a 10px margin, and set the input box width to 70%
st.markdown(
    """
    <style>
    .stTextInput {
        position: fixed;
        bottom: 10px;
        width: 70%;
        left: 50%;
        transform: translateX(-50%);
    }
    .stContainer {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }
    .stContainer > div {
        max-height: 70vh;
        overflow-y: auto;
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)