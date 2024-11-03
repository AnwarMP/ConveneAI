import os
from typing import Optional, List, Dict
from llama_index.llms.anthropic import Anthropic
from llama_index.llms.openai import OpenAI
from llama_index.core.agent import FunctionCallingAgent
from llama_index.core.llms import ChatMessage, LLM  # Added LLM import
from llama_index.core.tools import FunctionTool

from src.services.email_service import EmailService

import json
import re
from typing import Dict, Any
from src.utils import *
import google.generativeai as genai
from google.generativeai import caching
import datetime
import time


# Define a simple dummy function
def noop_function():
    """A no-operation function."""
    return {"status": "No operation performed"}

dummy_tool = FunctionTool.from_defaults(
    noop_function,
    name="NoOpTool",
    description="A dummy tool for testing purposes"
)

class MeetingAnalysisAgent:
    def __init__(self, llm_provider: str = "openai", api_key: Optional[str] = None):
        """Initialize the meeting analysis agent"""
        self.llm = self._initialize_llm(llm_provider, api_key)
        self.email_service = EmailService()
        self.agent = self._initialize_agent()

    def _initialize_llm(self, provider: str, api_key: Optional[str] = None) -> LLM:
        """Initialize the chosen LLM provider"""
        if provider == "openai":
            api_key = api_key or os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OpenAI API key must be provided")
            return OpenAI(
                model="gpt-4o-mini",
                api_key=api_key,
                temperature=0.1
            )
        elif provider == "anthropic":
            api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("Anthropic API key must be provided")
            return Anthropic(
                model="claude-3-5-sonnet-20241022",
                api_key=api_key
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    def _initialize_agent(self) -> FunctionCallingAgent:
        """Initialize the function calling agent with system prompt"""
        prefix_messages = [
            ChatMessage(
                role="system",
                content=(
                    "You are a professional meeting transcriptionist and analyst, specializing in creating "
                    "clear, concise, and actionable meeting summaries. When participants mention emails, "
                    "you should proactively find and reference them using the search_email tool.\n\n"

                    "ENSURE THAT YOU RETURN THE SUMMARY IN MARKDOWN FORMAT, ADD <br> TAGS BETWEEN SECTIONS.\n\n"
                    
                    "Format Requirements:\n"
                    "1. Start with a brief one-line meeting overview\n"
                    "2. Include only relevant sections from the following format (omit sections if no relevant content):\n\n"
                    

                    "### MEETING OVERVIEW (Required)\n"
                    "- Date: [Extract from timestamps]\n"
                    "- Attendees: [Names from transcript]\n"
                    

                    "### KEY POINTS (If substantive discussion occurred)\n"
                    "- Lead with the most critical information\n"
                    "- Use clear, direct language\n"
                    "- Highlight major developments or changes\n\n"
                    

                    "### DECISIONS & OUTCOMES (If any decisions were made)\n"
                    "- Document specific decisions made\n"
                    "- Note approved changes or directions\n"
                    "- Include any voted items\n\n"
                    

                    "### CRITICAL ACTION ITEMS (If tasks were assigned)\n"
                    "- [Owner] Action required - [Timeline if mentioned]\n"
                    "- Format as specific, assignable tasks\n"
                    "- Include any deadlines or dependencies\n\n"
                    

                    "### RISKS & CONCERNS (If any were raised)\n"
                    "- Document identified risks\n"
                    "- Note major concerns raised\n"
                    "- Include potential impacts\n\n"
                    

                    "### NEXT STEPS (If discussed)\n"
                    "- List immediate next actions\n"
                    "- Include follow-up meetings if mentioned\n"
                    "- Note pending decisions or discussions\n\n"
                    

                    "## REFERENCED EMAILS (Only if emails were mentioned)\n"
                    "- When emails are mentioned, use search_email tool to find and include details\n"
                    "- Include relevant context from found emails\n\n"
                    "- Include the link to the email in the summary\n\n"
                    
                    "Writing Guidelines:\n"
                    "1. Be concise and direct\n"
                    "2. Use professional language\n"
                    "3. Focus on actionable information\n"
                    "4. Maintain chronological order where relevant\n"
                    "5. Highlight changes from previous summary\n"
                    "6. Remove any speculative or unnecessary commentary\n"
                    "7. Use bullet points for clarity\n"
                    "8. Include specific metrics or numbers when mentioned\n\n"
                    
                    "When updating existing summaries:\n"
                    "- Integrate new information seamlessly\n"
                    "- Remove redundancies\n"
                    "- Mark significant updates or changes\n"
                    "- Maintain context from previous discussions\n"
                    "- Update action items and risks as they evolve\n"
                    
                    "Keep the style consistent and focus on clarity and brevity. Use markdown for formatting, and links"
                )
            )
        ]
        
        search_email_tool = FunctionTool.from_defaults(
            fn=self.email_service.search_emails,
            description="Search for an email using a Gmail query string. Returns the first matching email's details."
        )
        
        return FunctionCallingAgent.from_tools(
            tools=[search_email_tool],
            llm=self.llm,
            verbose=True,
            prefix_messages=prefix_messages
        )

    def process_segment(self, existing_summary: str, new_transcript: str, full_transcript: str = '') -> str:
        """
        Process a new transcript segment and update the summary
        
        Args:
            existing_summary: Current summary if any
            new_transcript: New transcript segment to analyze
            full_transcript: Complete transcript history
        """
        prompt = """
            Based on the following meeting information, create or update a professional meeting summary.

            Previous Summary:
            {existing_summary_text}

            Meeting History:
            {full_transcript_text}

            New Discussion:
            {new_transcript_text}

            Requirements:
            1. If this is a new meeting, include a complete Meeting Overview section
            2. If updating, maintain the existing structure while incorporating new information
            3. Highlight any significant changes or developments
            4. Ensure all action items have clear ownership
            5. Keep the summary professional and actionable
            6. Remove any redundant or outdated information
            7. Be concise and direct
            
            Just give me the updated summary in markdown format. No need to explain. Insert two new lines between sections.
        """.format(
            existing_summary_text=existing_summary or 'No previous summary.',
            full_transcript_text=full_transcript or 'No previous transcript.',
            new_transcript_text=new_transcript
        )

        response = self.agent.chat(prompt)
        return response.response


class GeminiAgent:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Gemini agent"""
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Google API key must be provided")
        genai.configure(api_key=self.api_key)
        self.model = None
        self.initialize_with_video( video_path='/Users/anwarmujeeb/Desktop/ConveneAI/src/v2.mp4')

    def initialize_with_video(self, video_path: str) -> None:
        """Initialize the model with video and cache it for 10 minutes"""
        # Upload video file
        video_file = genai.upload_file(path=video_path)

        # Wait for processing
        while video_file.state.name == 'PROCESSING':
            print('Waiting for video to be processed...')
            time.sleep(2)
            video_file = genai.get_file(video_file.name)

        print(f'Video processing complete: {video_file.uri}')

        # Create cache with 10 minute TTL
        cache = caching.CachedContent.create(
            model='models/gemini-1.5-flash-001',
            display_name='meeting_video',
            system_instruction="""You are an expert video analyzer, and your job is to answer 
            the user's query based on the video file you have access to.""",
            contents=[video_file],
            ttl=datetime.timedelta(minutes=10)
        )

        self.model = genai.GenerativeModel.from_cached_content(cached_content=cache)
        self.transcript = self.analyze_transcript()

    def analyze_transcript(self) -> str:
        """
        Analyze and enhance the recorded meeting transcript with timeout.
        """
        if not self.model:
            raise ValueError("Model not initialized with video")

        print(f"Inside of analyze_transcript()")

        prompt = f"""
        Please analyze and enhance this meeting transcript by:
        1. Add any timestamp to transcript
        2. Adding visual cues and gestures observed in the video:
        - Nodding or shaking head
        - Hand gestures
        - Pointing or presenting
        - Screen sharing activities
        - Any other notable visual interactions
        3. Clarifying speaker identification if unclear
        4. Noting any significant pauses or overlapping speech
        5. Adding context markers for better readability



        Raw Transcript:
        Matt: Hey John, thanks for meeting with me today. I'm excited to introduce you to our new product, Convene AI.

        John: Hi Matt! I've heard some buzz about Convene AI but would love to hear more from you. What sets it apart from other meeting tools out there?

        Matt: Great question! At its core, Convene AI is a meeting assistant, but it goes well beyond what other tools offer.

        John: How so?

        Matt: Well, during meetings, We provide real-time notes and insights. It doesn't just capture what's being said; it analyzes the conversation to highlight key points, decisions, and action items as they happen.

        John: That sounds incredibly useful. Keeping up with notes during intense discussions can be challenging.

        Matt: Exactly! And here's where we truly shine: it can search through your documents and emails in real-time to find relevant information during the meeting.

        John: Wait, so if we're discussing a project, it can pull up related documents or past emails on the spot?

        Matt: You've got it. No more digging through folders or inboxes mid-meeting. We bring the information right to you when you need it.

        John: That would definitely keep the meeting flow uninterrupted. What about scheduling? Can it help with that too?

        Matt: Absolutely. If you need to set up a follow-up meeting or schedule tasks, we can add calendar events directly from the meeting. It's all about streamlining the process.

        John: Impressive. Now, team dynamics are important to us. Can Convene AI help us understand participant engagement during meetings?

        Matt: Definitely. Using gesture and facial expression recognition, we can detect emotions among participants. This adds a new depth to sentiment analysis.

        John: [thumbs up]

        Matt: I know right? It ensures that everyone's on the same page and helps you address concerns in real-time.

        John: That's a game-changer. Looking for information after meetings is often a hassle. Does Convene AI assist there as well?

        Matt: Yes, it does. After the meeting, you can chat with the meeting video. If you have questions or need to revisit a specific point, just ask, and we will navigate to that exact moment. Also let me present something you.

        John: So it's like having a smart assistant that remembers everything and can pull up details on demand?

        Matt: Exactly! Plus, it adds more context and information to the notes, so your meeting summaries are comprehensive and actionable.

        John: This could really enhance our productivity. Integrating documents, emails, calendar events, real-time insights, emotion detection—it covers all bases.

        Matt: That's the goal.

        John: Alright, I'm sold. It was a pleasure meeting with you.

        Matt: Likewise. I'll send over more details and set up a demo for your team. Thanks for your time today.

        Please only return the enhanced transcript maintaining the original format but with visual cues 
        and corrections integrated naturally into the text. Keep timestamps in [HH:MM:SS] format.
        """
        print(f"Prompt: {prompt}")
        print("Enhancing transcript...")
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0,  # Slightly higher for more natural conversation
                    candidate_count=1,
                    max_output_tokens=1024,
                    top_p=0.8,
                    top_k=40
                )
            )
            return response.text
        
        except Exception as e:
            print(f"Error enhancing transcript: {str(e)}")
            return f"Error processing transcript: {str(e)}"

    def chat(self, prompt: str, chat_history: str = '') -> str:
        """
        Chat about the video/meeting using the cached model.
        
        Args:
            prompt: User's message or question
            chat_history: Previous chat messages for context
        
        Returns:
            str: Gemini's response
        """
        if not self.model:
            raise ValueError("Model not initialized with video")

        context = f"""
        Based on the video content and our previous discussion:
        {chat_history}

        Please respond to this message:
        {prompt}

        Consider:
        1. The visual content from the video
        2. Previous context from our chat
        3. Any relevant discussions or decisions made
        4. Specific details about what was shown or demonstrated
        
        Be specific and reference actual content from the video when relevant.
        """

        try:
            response = self.model.generate_content(
                context,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.2,  # Slightly higher for more natural conversation
                    candidate_count=1,
                    max_output_tokens=1024,
                    top_p=0.8,
                    top_k=40
                )
            )
            
            return response.text
        except Exception as e:
            print(f"Error generating chat response: {str(e)}")
            return f"Error processing message: {str(e)}"