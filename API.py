import os
from dotenv import load_dotenv
from sib_api_v3_sdk import Configuration, ApiClient, TransactionalEmailsApi, SendSmtpEmail
from manage_emails import get_emails, delete_emails_by_ids

# Load environment variables
load_dotenv()

# Configure API key with validation
api_key = os.getenv('BREVO_API_KEY')
if not api_key:
    raise ValueError("BREVO_API_KEY not found in environment variables")

configuration = Configuration()
configuration.api_key['api-key'] = api_key

def send_html_email(to_email, subject, html_content):
    try:
        api_instance = TransactionalEmailsApi(ApiClient(configuration))
        send_smtp_email = SendSmtpEmail(
            to=[{"email": to_email}],
            sender={"name": "ikhbarIA", "email": "ikhbarIA@gmail.com"},
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
def send_all_emails():
    current_directory = os.getcwd()

    # Specify your HTML file name or path
    html_folder = "html"

    # Combine the current directory with the HTML file path
    html_path = os.path.join(current_directory, html_folder)

    # Use absolute path or path relative to script location
    langs = [("ar", "arabic"), ("dr", "darija"), ("en", "english"), ("fr", "french")]
    templates = {}
    for code, language in langs :
        with open(os.path.join(html_path,f"generated_{code}.html"), "r") as f:
            templates[language] = f.read()
    print(templates)
    if not delete_emails_by_ids():
        print(" Problema mi amigo ")

    emails_df = get_emails()
    print(">"*50)
    print(emails_df)
    for i in emails_df.index:
        email = emails_df.loc[i, 'email']
        current_html = templates[emails_df.loc[i,"Language"]]
        current_html = current_html.replace("IDENTIFIANT", emails_df.loc[i,"Id"])
        current_html = current_html.replace("USERNAME", emails_df.loc[i,"Full Name"])
        send_html_email(email, "NewsLetter", current_html)


if __name__ == "__main__":
    send_all_emails()
# ! ===============
# * Translate templates
# * Make sure bli TheNexus kaytransliti **
# * kml dict dyal formHTML
