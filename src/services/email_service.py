from typing import List, Dict
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import os
import pickle
from pathlib import Path

class EmailService:
    """Simple Gmail service that returns first matching email"""
    
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    CREDENTIALS_DIR = Path('.credentials')
    
    def __init__(self):
        # Create credentials directory if it doesn't exist
        self.CREDENTIALS_DIR.mkdir(exist_ok=True)
        self.service = self._get_gmail_service()

    def _get_gmail_service(self):
        """Get Gmail API service using existing token.json"""
        token_path = self.CREDENTIALS_DIR / 'token.json'
        
        if not token_path.exists():
            raise FileNotFoundError(
                f"token.json not found at {token_path}. "
                "Please ensure the file exists in the .credentials directory."
            )

        # Load credentials from token.json
        with open(token_path, 'r') as token_file:
            token_data = json.load(token_file)
            
        creds = Credentials.from_authorized_user_info(token_data, self.SCOPES)
        
        # Refresh token if expired
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        return build('gmail', 'v1', credentials=creds)

    def search_emails(self, query: str) -> Dict:
        """Search emails and return first result for the query"""
        try:
            # Search for messages
            response = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=1  # Just get the first match
            ).execute()
            
            if 'messages' in response:
                # Get the first message's details
                msg_id = response['messages'][0]['id']
                msg = self.service.users().messages().get(
                    userId='me',
                    id=msg_id,
                    format='metadata',
                    metadataHeaders=['subject', 'from', 'date']
                ).execute()
                
                # Extract headers
                headers = msg['payload']['headers']
                subject = next(
                    (h['value'] for h in headers if h['name'].lower() == 'subject'),
                    '(no subject)'
                )
                sender = next(
                    (h['value'] for h in headers if h['name'].lower() == 'from'),
                    '(no sender)'
                )
                
                # Create result
                return {
                    'id': msg_id,
                    'subject': subject,
                    'from': sender,
                    # 'url': f"https://mail.google.com/mail/u/0/#inbox/{msg_id}",
                    'markdown_url': f"[{subject}](https://mail.google.com/mail/u/0/#inbox/{msg_id}",
                    'query_used': query
                }
                
        except Exception as e:
            print(f"Error searching emails: {e}")
            return None