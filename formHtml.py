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

def fill_email(template_path, template_data):
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
def get_content_safely(language):
    try:
        with open("D:/dev/projects/Las9/TGT.txt", "r", encoding='utf-8') as file:
            template_content = file.read()
        title = generate_title(template_content)
        content = summarize_news(template_content,language)
        return title, content
    except Exception as e:
        print(f"Error generating content: {e}")
        return "Latest Tech News", "<p>Content generation failed. Please check your content generation functions.</p>"

# Main execution
if __name__ == "__main__":
    # Generate title and content
    
    languages = [("Arabic","D:/dev/projects/ikhbarIA/TheNexus/NewsLetter/template_ar.html", "ar"), ("Moroccan Dialect","D:/dev/projects/ikhbarIA/TheNexus/NewsLetter/template_dr.html", "dr"), ("English","D:/dev/projects/ikhbarIA/TheNexus/NewsLetter/template_en.html", "en"), ("French","D:/dev/projects/ikhbarIA/TheNexus/NewsLetter/template_fr.html", "fr")]

    for lang, path, code in languages:
        title, content = get_content_safely(lang)
        
        # Template data with Markdown support
        template_data = {
            'company_name': 'Made in Morocco AI',
            'title': title,
            'category': 'Technology',
            'content': content,
            'address': 'MOROCCO, RABAT, ENSAM, INDIA 2027'
        }
        # Render email HTML
        html_page = fill_email(
            template_path=path,
            template_data=template_data
        )

        # Save the generated HTML
        if html_page:
            with open(f"generated_{code}.html", "w", encoding="utf-8") as f:
                f.write(html_page)
