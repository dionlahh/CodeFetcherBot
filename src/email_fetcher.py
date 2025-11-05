"""
Email fetcher for retrieving Netflix verification emails
"""

import imaplib
import email
import logging
from email.header import decode_header
import re
from typing import Optional
from .constants import NETFLIX_EMAIL_SENDER, NETFLIX_EMAIL_SUBJECT, ERROR_NO_NETFLIX_EMAILS

logger = logging.getLogger(__name__)

class EmailFetcher:
    """Handles email fetching operations"""
    
    def __init__(self, server: str, port: int, email_addr: str, password: str):
        self.server = server
        self.port = port
        self.email_addr = email_addr
        self.password = password
    
    def fetch_latest_email(self) -> Optional[dict]:
        """
        Fetch the latest email from the configured email account
        
        Returns:
            dict: Email data with 'subject', 'sender', 'date', and 'body'
            None: If no emails found or error occurred
        """
        try:
            # Connect to the email server
            mail = imaplib.IMAP4_SSL(self.server, self.port)
            mail.login(self.email_addr, self.password)
            
            # Select the inbox
            mail.select("inbox")
            
            # Search for Netflix verification code emails
            search_criteria = f'(FROM "{NETFLIX_EMAIL_SENDER}" SUBJECT "{NETFLIX_EMAIL_SUBJECT}")'
            status, messages = mail.search(None, search_criteria)
            
            if status != "OK" or not messages[0]:
                logger.warning(ERROR_NO_NETFLIX_EMAILS)
                return None
            
            # Get the latest email (last in the list)
            email_ids = messages[0].split()
            if not email_ids:
                logger.warning(ERROR_NO_NETFLIX_EMAILS)
                return None
                
            latest_email_id = email_ids[-1]
            
            # Fetch the email
            status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
            
            if status != "OK":
                logger.error("Failed to fetch email")
                return None
            
            # Parse the email
            email_body = msg_data[0][1]
            email_message = email.message_from_bytes(email_body)
            
            # Extract email information
            subject = self._decode_subject(email_message["Subject"])
            sender = email_message["From"]
            date = email_message["Date"]
            
            # Extract email body
            body = self._extract_body(email_message)
            
            mail.logout()
            
            return {
                "subject": subject,
                "sender": sender,
                "date": date,
                "body": body
            }
            
        except Exception as e:
            logger.error(f"Error fetching email: {str(e)}")
            return None
    
    def _decode_subject(self, subject: str) -> str:
        """Decode email subject if it's encoded"""
        if subject:
            decoded_pairs = decode_header(subject)
            decoded_subject = ""
            for content, encoding in decoded_pairs:
                if isinstance(content, bytes):
                    decoded_subject += content.decode(encoding or 'utf-8')
                else:
                    decoded_subject += content
            return decoded_subject
        return "No Subject"
    
    def _extract_body(self, email_message) -> str:
        """Extract the body content from email message"""
        body = ""
        
        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                # Skip attachments
                if "attachment" not in content_disposition:
                    if content_type == "text/plain":
                        try:
                            body = part.get_payload(decode=True).decode('utf-8')
                            break
                        except:
                            body = part.get_payload(decode=True).decode('latin-1', errors='ignore')
                            break
                    elif content_type == "text/html" and not body:
                        try:
                            html_body = part.get_payload(decode=True).decode('utf-8')
                            # Simple HTML to text conversion (remove tags)
                            body = re.sub('<[^<]+?>', '', html_body)
                        except:
                            pass
        else:
            try:
                body = email_message.get_payload(decode=True).decode('utf-8')
            except:
                body = email_message.get_payload(decode=True).decode('latin-1', errors='ignore')
        
        return body.strip() if body else "No content available"