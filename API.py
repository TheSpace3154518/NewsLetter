import os
import time
import logging
from typing import Dict, List, Optional, Tuple, Union
import pandas as pd
from dotenv import load_dotenv
from sib_api_v3_sdk import Configuration, ApiClient, TransactionalEmailsApi, SendSmtpEmail
from TheNexusModule.manage_emails import get_emails, delete_emails_by_ids
from functools import lru_cache

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("newsletter_sender.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("newsletter_api")

# Load environment variables
load_dotenv()

class EmailSender:
    def __init__(self, sender_name: str = "IkhbarIA Newsletter", sender_email: str = "ikhbaria1@gmail.com"):
        # Configure API key with validation
        self.api_key = os.getenv('BREVO_API_KEY')
        if not self.api_key:
            raise ValueError("BREVO_API_KEY not found in environment variables")

        self.configuration = Configuration()
        self.configuration.api_key['api-key'] = self.api_key
        self.api_instance = TransactionalEmailsApi(ApiClient(self.configuration))
        self.sender = {"name": sender_name, "email": sender_email}
        self.max_retries = 3
        self.retry_delay = 2  # seconds
        self.results = {"success": [], "failed": []}
        # Cache templates on initialization
        self.templates = {}

    def send_html_email(self, to_email: str, subject: str, html_content: str, max_retries: int = None) -> dict:
        """Send HTML email to a single recipient with retry logic"""
        if max_retries is None:
            max_retries = self.max_retries

        # Basic email validation
        if not to_email or '@' not in to_email:
            logger.error(f"Invalid email address: {to_email}")
            self.results["failed"].append({"email": to_email, "reason": "Invalid email format"})
            return {"error": "Invalid email format"}

        # Attempt to send with retries
        for attempt in range(max_retries):
            try:
                send_smtp_email = SendSmtpEmail(
                    to=[{"email": to_email}],
                    sender=self.sender,
                    subject=subject,
                    html_content=html_content
                )

                response = self.api_instance.send_transac_email(send_smtp_email)
                logger.info(f"Email sent successfully to {to_email}")
                self.results["success"].append(to_email)
                return response
            except Exception as e:
                logger.warning(f"Attempt {attempt+1}/{max_retries} failed for {to_email}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    logger.error(f"Failed to send email to {to_email} after {max_retries} attempts: {e}")
                    self.results["failed"].append({"email": to_email, "reason": str(e)})
                    return {"error": str(e)}

    def _read_file_safely(self, file_path: str, default="") -> str:
        """Safely read file content with proper error handling"""
        try:
            with open(file_path, "r", encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            logger.warning(f"File not found: {file_path}")
            return default
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return default

    def load_templates(self, html_folder: str = "TheNexusModule/html", force_reload: bool = False) -> Dict[str, str]:
        """Load all email templates from the specified folder"""
        # Return cached templates if available and not forced to reload
        if self.templates and not force_reload:
            return self.templates

        current_directory = os.getcwd()
        html_path = os.path.join(current_directory, html_folder)

        langs = [("ar", "arabic"), ("dr", "darija"), ("en", "english"), ("fr", "french")]
        self.templates = {}

        for code, language in langs:
            template_path = os.path.join(html_path, f"generated_{code}.html")
            css_path = os.path.join(html_path, "style.css")

            # Read HTML content
            html_content = self._read_file_safely(template_path)
            if not html_content:
                logger.error(f"Template file not found or empty: {template_path}")
                self.templates[language] = ""
                continue

            # Read CSS content
            css_content = self._read_file_safely(css_path)
            if css_content:
                logger.info(f"Loaded CSS for {language}")

                # Inject CSS into HTML using optimized approach
                if "<!-- CSS_STYLES -->" in html_content:
                    html_content = html_content.replace("<!-- CSS_STYLES -->", f"<style>\n{css_content}\n</style>")
                elif "<head>" in html_content:
                    html_content = html_content.replace("<head>", f"<head>\n<style>\n{css_content}\n</style>")
                else:
                    html_content = f"<style>\n{css_content}\n</style>\n{html_content}"

            self.templates[language] = html_content
            logger.info(f"Loaded template for {language}")

        return self.templates

    def personalize_template(self, template: str, user_data: Dict[str, str]) -> str:
        """Personalize template with user data"""

        if not template:
            return ""

        html_folder = "TheNexusModule/html"
        current_directory = os.getcwd()
        html_path = os.path.join(current_directory, html_folder)
        js_path = os.path.join(html_path, "script.js")
        with open(js_path,"r") as f :
            script = f.read()
        # Use single pass replacement for performance
        replacements = {
            "IDENTIFIANT": str(user_data.get("Id", "")),
            "USERNAME": str(user_data.get("Full Name", "")),
            "SCRIPT": script,
        }

        result = template
        for placeholder, value in replacements.items():
            result = result.replace(placeholder, value)

        return result

    def send_all_emails(self, subject: str = "NewsLetter") -> Dict[str, List]:
        """Send emails to all recipients from the database"""
        # Reset results
        self.results = {"success": [], "failed": []}

        # Load templates if not already loaded
        if not self.templates:
            self.load_templates()

        # Delete previous emails if needed
        try:
            delete_emails_by_ids()
        except Exception as e:
            logger.error(f"Failed to delete previous emails: {e}")

        # Get email recipients
        try:
            emails_df = get_emails()
            logger.info(f"Retrieved {len(emails_df)} email recipients")
        except Exception as e:
            logger.error(f"Failed to get email recipients: {e}")
            return self.results

        # Send emails to each recipient
        for i in emails_df.index:
            try:
                email = emails_df.loc[i, 'email']
                language = emails_df.loc[i, "Language"]

                if language not in self.templates or not self.templates[language]:
                    logger.warning(f"No template found for language: {language}. Skipping {email}")
                    self.results["failed"].append({"email": email, "reason": f"No template for language: {language}"})
                    continue

                user_data = {
                    "Id": emails_df.loc[i, "Id"],
                    "Full Name": emails_df.loc[i, "Full Name"]
                }

                personalized_html = self.personalize_template(self.templates[language], user_data)
                self.send_html_email(email, subject, personalized_html)

            except Exception as e:
                email = emails_df.loc[i, 'email'] if 'i' in locals() and i in emails_df.index else "unknown"
                logger.error(f"Error processing recipient {email}: {e}")
                self.results["failed"].append({"email": email, "reason": str(e)})

        # Report results
        logger.info(f"Email sending complete. Success: {len(self.results['success'])}, Failed: {len(self.results['failed'])}")
        return self.results


def send_all_emails():
    """Backward compatible function to send all emails"""
    sender = EmailSender()
    return sender.send_all_emails()


if __name__ == "__main__":
    send_all_emails()
