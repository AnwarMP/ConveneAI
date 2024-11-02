import os
from typing import Optional
from llama_index.llms.anthropic import Anthropic
from llama_index.core.agent import FunctionCallingAgent
from llama_index.core.llms import ChatMessage

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
