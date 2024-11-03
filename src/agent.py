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
                model="gpt-4",
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
                    
                    "Format Requirements:\n"
                    "1. Start with a brief one-line meeting overview\n"
                    "2. Include only relevant sections from the following format (omit sections if no relevant content):\n\n"
                    
                    "MEETING OVERVIEW (Required)\n"
                    "- Date: [Extract from timestamps]\n"
                    "- Attendees: [Names from transcript]\n"
                    
                    "KEY POINTS (If substantive discussion occurred)\n"
                    "- Lead with the most critical information\n"
                    "- Use clear, direct language\n"
                    "- Highlight major developments or changes\n\n"
                    
                    "DECISIONS & OUTCOMES (If any decisions were made)\n"
                    "- Document specific decisions made\n"
                    "- Note approved changes or directions\n"
                    "- Include any voted items\n\n"
                    
                    "CRITICAL ACTION ITEMS (If tasks were assigned)\n"
                    "- [Owner] Action required - [Timeline if mentioned]\n"
                    "- Format as specific, assignable tasks\n"
                    "- Include any deadlines or dependencies\n\n"
                    
                    "RISKS & CONCERNS (If any were raised)\n"
                    "- Document identified risks\n"
                    "- Note major concerns raised\n"
                    "- Include potential impacts\n\n"
                    
                    "NEXT STEPS (If discussed)\n"
                    "- List immediate next actions\n"
                    "- Include follow-up meetings if mentioned\n"
                    "- Note pending decisions or discussions\n\n"
                    
                    "REFERENCED EMAILS (Only if emails were mentioned)\n"
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
                    
                    "Keep the style consistent and focus on clarity and brevity."
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
            
            Just give me the updated summary in format mentioned above. No need to explain. Insert a new line between sections.
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
            model='models/gemini-1.5-pro-latest',
            display_name='meeting_video',
            system_instruction="""You are an expert video analyzer, and your job is to answer 
            the user's query based on the video file you have access to.""",
            contents=[video_file],
            ttl=datetime.timedelta(minutes=10)
        )

        self.model = genai.GenerativeModel.from_cached_content(cached_content=cache)

    def analyze_transcript(self, transcript: str) -> str:
        """Analyze transcript for correctness and add visual cues"""
        if not self.model:
            raise ValueError("Model not initialized with video")

        prompt = f"""
        I have a transcript for this video.
        {transcript}

        Go through the transcript and the timestamps. Make sure they are correct. 
        If not, fix them. Also try detecting specific head and hand gestures, 
        such as nodding and shaking and thumbs up and down, during a video-recorded meeting and add them 
        to the transcript if detected.
        """

        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(temperature=0.0)
        )
        
        return response.text

    def chat(self, prompt: str) -> str:
        """Chat about the video using the cached model"""
        if not self.model:
            raise ValueError("Model not initialized with video")

        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(temperature=0.0)
        )
        
        return response.text
    