import os
from dotenv import load_dotenv
from sib_api_v3_sdk import Configuration, ApiClient, TransactionalEmailsApi, SendSmtpEmail

# Load environment variables
load_dotenv()

# Configure API key with validation
api_key = os.getenv('BREVO_API_KEY')
if not api_key:
    raise ValueError("BREVO_API_KEY not found in environment variables")

configuration = Configuration()
configuration.api_key['api-key'] = api_key

def send_html_email(to_email, subject, html_file_path):
    try:
        # Convert to absolute path if it's not already
        if not os.path.isabs(html_file_path):
            html_file_path = os.path.join(os.path.dirname(__file__), html_file_path)
        
        # Verify file exists
        if not os.path.exists(html_file_path):
            raise FileNotFoundError(f"HTML file not found: {html_file_path}")
            
        # Read HTML file
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
            
        api_instance = TransactionalEmailsApi(ApiClient(configuration))
        send_smtp_email = SendSmtpEmail(
            to=[{"email": to_email}],
            sender={"name": "MadeInMorocco", "email": "madeinmoroccoai@gmail.com"},
            subject=subject,
            html_content=html_content
        )
        
        response = api_instance.send_transac_email(send_smtp_email)
        print(f"Email sent successfully to {to_email}")
        return response
    except Exception as e:
        print(f"Error sending email: {e}")
        # Return error information instead of raising
        return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    # Use absolute path or path relative to script location
    html_file = os.path.join(os.path.dirname(__file__), "anas_generated_html.html")
    send_html_email("anass.amchaar14@gmail.com", "HTML Email", html_file)
    