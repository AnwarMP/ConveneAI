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
                    "You are a professional meeting transcriptionist and analyst, specializing in creating "
                    "clear, concise, and actionable meeting summaries. Focus on capturing key information "
                    "while maintaining a professional tone.\n\n"
                    
                    "Format Requirements:\n"
                    "1. Start with a brief one-line meeting overview\n"
                    "2. Follow with structured sections using the following format:\n\n"
                    
                    "MEETING OVERVIEW\n"
                    "- Date: [Extract from timestamps]\n"
                    "- Attendees: [Names from transcript]\n"
                    "- Duration: [Calculate from timestamps]\n\n"
                    
                    "KEY POINTS\n"
                    "- Lead with the most critical information\n"
                    "- Use clear, direct language\n"
                    "- Highlight major developments or changes\n\n"
                    
                    "DECISIONS & OUTCOMES\n"
                    "- Document specific decisions made\n"
                    "- Note approved changes or directions\n"
                    "- Include any voted items\n\n"
                    
                    "CRITICAL ACTION ITEMS\n"
                    "- [Owner] Action required - [Timeline if mentioned]\n"
                    "- Format as specific, assignable tasks\n"
                    "- Include any deadlines or dependencies\n\n"
                    
                    "RISKS & CONCERNS\n"
                    "- Document identified risks\n"
                    "- Note major concerns raised\n"
                    "- Include potential impacts\n\n"
                    
                    "NEXT STEPS\n"
                    "- List immediate next actions\n"
                    "- Include follow-up meetings if mentioned\n"
                    "- Note pending decisions or discussions\n\n"
                    
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
        
        return FunctionCallingAgent.from_tools(
            tools=[dummy_tool],
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
        prompt = (
            "Based on the following meeting information, create or update a professional meeting summary.\n\n"
            
            f"Previous Summary:\n{existing_summary or 'No previous summary.'}\n\n"
            
            f"Meeting History:\n{full_transcript or 'No previous transcript.'}\n\n"
            
            f"New Discussion:\n{new_transcript}\n\n"
            
            "Requirements:\n"
            "1. If this is a new meeting, include a complete Meeting Overview section\n"
            "2. If updating, maintain the existing structure while incorporating new information\n"
            "3. Highlight any significant changes or developments\n"
            "4. Ensure all action items have clear ownership\n"
            "5. Keep the summary professional and actionable\n"
            "6. Remove any redundant or outdated information\n"
            "7. Be concise and direct\n"
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