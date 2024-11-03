from typing import List, Dict, Optional
from datetime import datetime, timedelta

class EmailQueryGenerator:
    """Generate Gmail search queries based on transcript context"""
    
    def __init__(self):
        self.date_keywords = {
            "yesterday": 1,
            "last week": 7,
            "last month": 30,
            "today": 0
        }

    def parse_date_reference(self, text: str) -> Dict[str, str]:
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

    def generate_queries(self, analysis_result: Dict) -> List[str]:
        """
        Generate Gmail search queries based on LLM analysis
        
        Args:
            analysis_result: Dict containing:
                - sender: str
                - recipients: List[str]
                - subject: str
                - date_range: Dict[str, str]
                - attachment_type: str
                
        Returns:
            List of Gmail search query strings
        """
        queries = []
        
        # Extract components with safe gets
        sender = analysis_result.get("sender", "")
        recipients = analysis_result.get("recipients", [])
        subject = analysis_result.get("subject", "")
        attachment_type = analysis_result.get("attachment_type", "")
        date_range = analysis_result.get("date_range", {})
        
        # Build base query
        if sender:
            base_query = f"from:{sender}"
            queries.append(base_query)
            
            # Add recipient if available
            if recipients:
                for recipient in recipients:
                    queries.append(f"{base_query} to:{recipient}")
            
            # Add subject if available
            if subject:
                queries.append(f"{base_query} subject:({subject})")
            
            # Add attachment info if available
            if attachment_type:
                queries.append(f"{base_query} has:attachment filename:{attachment_type}")
        
        # Add date constraints
        if date_range:
            date_parts = []
            if date_range.get("after"):
                date_parts.append(f"after:{date_range['after']}")
            if date_range.get("before"):
                date_parts.append(f"before:{date_range['before']}")
            
            if date_parts:
                date_str = " ".join(date_parts)
                # Add dates to existing queries
                new_queries = []
                for query in queries:
                    new_queries.append(f"{query} {date_str}")
                queries.extend(new_queries)
        
        return queries if queries else [""]  # Return empty query if no components found