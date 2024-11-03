from datetime import datetime, timedelta
from typing import Dict, Optional

class ContextProvider:
    """Provides contextual information for email analysis"""
    
    def __init__(self):
        self.date_keywords = {
            "yesterday": 1,
            "last week": 7,
            "last month": 30,
            "today": 0
        }
    
    def get_current_context(self) -> Dict:
        """Get current date-time context"""
        now = datetime.now()
        return {
            "current_date": now.strftime("%Y/%m/%d"),
            "current_time": now.strftime("%H:%M:%S"),
            "current_day": now.strftime("%A"),
            "yesterday": (now - timedelta(days=1)).strftime("%Y/%m/%d"),
            "last_week": (now - timedelta(days=7)).strftime("%Y/%m/%d"),
            "last_month": (now - timedelta(days=30)).strftime("%Y/%m/%d")
        }

    def parse_date_reference(self, text: str) -> Dict[str, Optional[str]]:
        """Parse relative date references into Gmail date formats"""
        today = datetime.now()
        
        # Check for specific date references
        for keyword, days in self.date_keywords.items():
            if keyword in text.lower():
                if days == 0:  # today
                    date = today
                else:
                    date = today - timedelta(days=days)
                    
                # For ranges like "last week", "last month"
                if keyword in ["last week", "last month"]:
                    return {
                        "after": (date - timedelta(days=7 if keyword == "last week" else 30)).strftime("%Y/%m/%d"),
                        "before": today.strftime("%Y/%m/%d")
                    }
                else:  # for specific days like "yesterday"
                    return {
                        "after": date.strftime("%Y/%m/%d"),
                        "before": (date + timedelta(days=1)).strftime("%Y/%m/%d")
                    }
        
        return {"after": None, "before": None}

    @staticmethod
    def format_date_for_query(date_str: Optional[str]) -> str:
        """Format a date string for Gmail query"""
        try:
            date = datetime.strptime(date_str, "%Y/%m/%d")
            return date.strftime("%Y/%m/%d")
        except (ValueError, TypeError):
            return ""