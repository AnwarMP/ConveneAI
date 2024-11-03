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
            tools=[],  # Tools will be added later
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
    """Agent specifically designed for generating email queries from transcripts"""
    """Agent specifically designed for generating email queries from transcripts"""
    
    def __init__(self, llm_provider: str = "openai", api_key: Optional[str] = None):
        """
        Initialize the email query agent
        
        Args:
            llm_provider: "openai" or "anthropic"
            api_key: Optional API key (will use environment variable if not provided)
        """
        self.llm = self._initialize_llm(llm_provider, api_key)
        self.query_generator = EmailQueryGenerator()
        self.email_service = EmailService()
        self.context_provider = ContextProvider()
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
        """Initialize the function calling agent with email-specific system prompt"""
        prefix_messages = [
            ChatMessage(
                role="system",
                content=(
                    "You are an AI assistant specialized in analyzing meeting transcripts "
                    "to identify and generate relevant email search queries. Your task is "
                    "to extract email references and return them in a structured format.\n\n"
                    
                    "You will receive:\n"
                    "1. Current date context\n"
                    "2. A transcript segment\n\n"
                    
                    "When analyzing transcripts, focus on:\n"
                    "- Explicit mentions of emails ('that email from John')\n"
                    "- Time references ('sent last week', 'from yesterday')\n"
                    "- Subject matter ('about the Q4 review')\n"
                    "- Sender/recipient information ('from Sarah to the team')\n"
                    "- Attachment mentions ('with the PDF attached')\n\n"
                    
                    "Return the analysis as a structured JSON object with:\n"
                    "- sender: The email sender's name\n"
                    "- recipients: List of recipients or teams\n"
                    "- subject: Email subject or topic\n"
                    "- date_range: Dictionary with 'after' and 'before' dates\n"
                    "- attachment_type: File extension or type if mentioned\n"
                )
            )
        ]

        tools = [
            FunctionTool.from_defaults(
                fn=self._generate_email_queries,
                name="generate_email_queries",
                description="Generate Gmail search queries from structured email data"
            ),
            FunctionTool.from_defaults(
                fn=self._extract_date_context,
                name="extract_date_context",
                description="Extract and standardize date references using current context"
            )
        ]
        
        return FunctionCallingAgent.from_tools(
            tools=tools,
            llm=self.llm,
            verbose=True,
            prefix_messages=prefix_messages
        )

    def _generate_email_queries(self, analysis_result: Dict) -> Dict[str, List[str]]:
        """Generate Gmail search queries based on structured analysis"""
        queries = self.query_generator.generate_queries(analysis_result)
        return {
            "context": "Email reference identified in transcript",
            "queries": queries
        }

    def _extract_date_context(self, text: str) -> Dict[str, Optional[str]]:
        """Extract date-related information from transcript"""
        return self.context_provider.parse_date_reference(text)


    async def analyze_transcript_segment(self, transcript: str) -> Dict[str, Any]:
        """Analyze a transcript segment and generate email queries"""
        
        # Get current context
        context = self.context_provider.get_current_context()
        
        prompt = (
            f"Current date context:\n"
            f"- Today: {context['current_date']} ({context['current_day']})\n"
            f"- Yesterday: {context['yesterday']}\n"
            f"- Last week started: {context['last_week']}\n\n"
            f"Please analyze this transcript segment and return ONLY a JSON object with "
            f"the following structure. No other text or explanation:\n\n"
            "{\n"
            '  "sender": "name",\n'
            '  "recipients": ["list", "of", "recipients"],\n'
            '  "subject": "subject line",\n'
            '  "date_range": {"after": "YYYY/MM/DD", "before": "YYYY/MM/DD"},\n'
            '  "attachment_type": "file extension"\n'
            "}\n\n"
            f"Transcript to analyze:\n{transcript}"
        )

        response = self.agent.chat(prompt)
        
        try:
            # Extract JSON from response
            if isinstance(response.response, str):
                # Find JSON pattern using regex
                json_match = re.search(r'({[\s\S]*})', response.response)
                if json_match:
                    json_str = json_match.group(1)
                    analysis_result = json.loads(json_str)
                else:
                    raise ValueError("No JSON object found in response")
            else:
                analysis_result = response.response

            # Generate queries from the parsed result
            queries = self.query_generator.generate_queries(analysis_result)
            
            return {
                "analysis": analysis_result,
                "queries": queries,
                "context": context,
                "confidence": 0.8
            }
        except Exception as e:
            return {
                "error": f"Failed to generate queries: {str(e)}",
                "raw_response": response.response,
                "context": context,
                "confidence": 0.5
            }

    async def search_emails(self, queries: List[str]) -> List[Dict]:
        """
        Search emails using the generated queries
        
        Args:
            queries: List of Gmail search queries
            
        Returns:
            List of matching email metadata
        """
        return await self.email_service.search_emails(queries)