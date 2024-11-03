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
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the meeting analysis agent"""
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:    
            raise ValueError("Anthropic API key must be provided")

        self.llm = Anthropic(
            model="claude-3-5-sonnet-20241022",
            api_key=self.api_key
        )
        
        self.agent = self._initialize_agent()

    def _initialize_agent(self) -> FunctionCallingAgent:
        """Initialize the function calling agent with system prompt"""
        prefix_messages = [
            ChatMessage(
                role="system",
                content=(
                    "You are a real-time meeting analysis assistant. Your task is to process "
                    "new meeting transcript segments and update the existing summary. "
                    
                    "You will receive:"
                    "1. The existing summary (if any)"
                    "2. A new transcript segment"
                    
                    "Provide an updated summary that:"
                    "- Incorporates new information with existing points"
                    "- Removes redundancies"
                    "- Updates existing points with new context"
                    "- Maintains clear, concise bullet points"
                    
                    "Format the output into these sections (only when relevant):"
                    "• Summary Points:"
                    "• Action Items:"
                    "• Decisions Made:"
                    "• Questions Raised:"
                    "• Follow-up Required:"
                    
                    "Keep the style consistent and focus on clarity and brevity."
                )
            )
        ]
        
        return FunctionCallingAgent.from_tools(
            tools=[dummy_tool],
            llm=self.llm,
            verbose=True,
            prefix_messages=prefix_messages
        )

    def process_segment(self, existing_summary: str, new_transcript: str) -> str:
        """Process a new transcript segment and update the summary"""
        prompt = (
            f"Existing Summary:\n{existing_summary or 'No existing summary.'}\n\n"
            f"New Transcript Segment:\n{new_transcript}\n\n"
            "Please provide an updated summary incorporating the new information."
        )

        response = self.agent.chat(prompt)
        return response.response
class EmailQueryAgent:
    def __init__(self, llm_provider: str = "openai", api_key: Optional[str] = None):
        """Initialize email query agent"""
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
        """Initialize the agent with email search prompts"""
        prefix_messages = [
            ChatMessage(
                role="system",
                content=(
                    "You are an AI assistant that helps find emails by creating Gmail search queries. "
                    "Given a conversation snippet, create a simple Gmail query. "
                    "\n\nRules:"
                    "\n- If someone mentions an email from a person, use 'from:person'"
                    "\n- If they mention a subject, add 'subject:topic'"
                    "\n- Keep queries simple and direct"
                    "\n- Return ONLY the query string, no other text"
                )
            )
        ]
        
        return FunctionCallingAgent.from_tools(
            tools=[],
            llm=self.llm,
            verbose=True,
            prefix_messages=prefix_messages
        )

    async def analyze_transcript_segment(self, transcript: str) -> Dict[str, Any]:
        """Find relevant email from transcript segment"""
        try:
            # Generate simple search query
            response = self.agent.chat(transcript)
            query = response.response.strip()
            
            # Search emails using query
            results = await self.email_service.search_emails([query])
            
            if results and len(results) > 0:
                return {
                    'status': 'success',
                    'query_used': query,
                    'email_found': results[0]
                }
            else:
                return {
                    'status': 'no_results',
                    'query_used': query
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }