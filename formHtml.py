import smtplib
import datetime
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import jinja2
from jinja2 import Template, Environment, FileSystemLoader
from TheNexus import generate_title, summarize_news
import markdown

def generate_logs(*args):
    print("\n".join(args))
    pass

def fill_email(recipient_email, subject, template_path, template_data):
    """
    Send an HTML email using a Jinja2 template with Markdown rendering.

    Args:
        recipient_email (str): Email address to send to.
        subject (str): Email subject line.
        template_path (str): Path to the HTML template file.
        template_data (dict): Data to render in the template.
    """
    
    # Add current year & date
    template_data['current_year'] = datetime.datetime.now().year
    template_data['date'] = datetime.datetime.now().strftime('%B %d, %Y')
    
    try:
        env = Environment(loader=FileSystemLoader(os.path.dirname(template_path)))

        # Register Markdown filter
        env.filters['markdown'] = lambda text: markdown.markdown(str(text))

        # Load the template
        template = env.get_template(os.path.basename(template_path))

        # Render template with Markdown support
        html_content = template.render(**template_data)      
        print(f"{html_content}")
        return html_content
        
    except FileNotFoundError:
        generate_logs("fill_html", "FileNotFound", f"Template file not found: {template_path}")
        return False
    except jinja2.exceptions.TemplateError as e:
        generate_logs(f"Template rendering error: {e}")
        return False
    except Exception as e:
        generate_logs(f"Failed to send email: {e}")
        return False

# Generate content with error handling
def get_content_safely():
    try:
        with open("D:/dev/projects/Las9/TGT.txt", "r", encoding='utf-8') as file:
            template_content = file.read()
        title = generate_title(template_content)
        content = summarize_news(template_content)
        return title, content
    except Exception as e:
        print(f"Error generating content: {e}")
        return "Latest Tech News", "<p>Content generation failed. Please check your content generation functions.</p>"

# Main execution
if __name__ == "__main__":
    # Generate title and content
    title, content = get_content_safely()
    
    # Template data with Markdown support
    template_data = {
        'company_name': 'Made in Morocco AI',
        'title': title,
        'category': 'Technology',
        'content': content,  # Markdown will be applied automatically
        'address': '123 Tech Street, Innovation City, TC 12345',
        'unsubscribe_link': 'https://example.com/unsubscribe'
    }
    
    # Render email HTML
    html_page = fill_email(
        recipient_email="anass.amchaar14@gmail.com",
        subject=f"Latest Tech Newsletter: {title}",
        template_path="D:/dev/projects/ikhbarIA/TheNexus/NewsLetter/template.html",
        template_data=template_data
    )

    # Save the generated HTML
    if html_page:
        with open("anas_generated_html.html", "w", encoding="utf-8") as f:
            f.write(html_page)
