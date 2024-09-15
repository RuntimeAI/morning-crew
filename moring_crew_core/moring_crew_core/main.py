from role import Role
from conversable_crew import ConversableCrew  # Make sure this import is correct
from skillset import Skillset
from config.settings import DEFAULT_MODEL
from skillsets.internet_search import InternetSearch
from skillsets.twitter_search import TwitterSearch
from skillsets.meeting_notes_draft import MeetingNotesDraft  # Import the new skillset

def main():
    # Create skillsets
    research_skill = Skillset("Research", "Conduct online research on various topics")
    writing_skill = Skillset("Writing", "Create well-written content based on research")
    internet_skillset = InternetSearch(debug=True, answer_num=5)
    twitter_search = TwitterSearch(debug=True, tweet_num=5)
    meeting_notes_draft = MeetingNotesDraft(debug=True)  # Initialize the new skillset

    # Create roles
    researcher = Role(
        personal_info={"name": "Researcher", "description": "Expert in conducting research"},
        skillsets=[research_skill]
    )
    content_writer = Role(
        personal_info={"name": "Content Writer", "description": "Skilled in creating engaging content"},
        skillsets=[writing_skill]
    )
    financial_researcher = Role(
        personal_info={
            "name": "Financial Researcher",
            "alias": "Taylor Masion",
            "description": "Specializing in Social Media and Sentiment Analysis, A highly skilled financial research expert with a strong ability to gather and analyze information from diverse internet sources, including social media platforms like Twitter. Proficient in conducting social media sentiment analysis to assess market sentiment, trends, and public opinion on relevant financial topics. With expertise in leveraging advanced analytical frameworks, this professional integrates sentiment analysis into broader financial evaluations to provide accurate investment recommendations and risk control strategies. Their insights help identify potential opportunities and mitigate risks, ensuring well-informed decisions for investors and stakeholders."
        },
        skillsets=[internet_skillset, twitter_search]
    )
    analyst_intern = Role(
        personal_info={
            "name": "Analyst Intern",
            "alias": "Ben Kim",
            "description": "Analyst Intern – Specializing in Meeting Notes Consolidation and Action Plan Management. A dedicated Analyst Intern responsible for consolidating detailed meeting notes from the trading team, ensuring key takeaways are accurately captured and organized. Skilled in drafting comprehensive reports that summarize discussions and decisions made during trading crew meetings, this professional also creates and manages action plans to support the trading team’s execution of tasks and strategies. With strong attention to detail and excellent communication skills, they ensure that critical information is clearly conveyed and actionable, facilitating efficient follow-through on the team’s trading objectives."
        },
        skillsets=[writing_skill, meeting_notes_draft]  # Add the new skillset to the analyst intern
    )

    # Create ConversableCrew with the default model
    crew = ConversableCrew([researcher, content_writer, financial_researcher, analyst_intern], model_index=DEFAULT_MODEL)

    # Simulate user interaction
    while True:
        user_input = input("Enter your instruction (or 'quit' to exit): ")
        if user_input.lower() == 'quit':
            break
        
        response = crew.instruction(user_input)
        print(f"Response: {response}")

if __name__ == "__main__":
    main()