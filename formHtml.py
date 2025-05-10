import datetime
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import jinja2
from jinja2 import Template, Environment, FileSystemLoader
from TheNexusModule.TheNexus import generate_title, summarize_news
import time
import re
from bs4 import BeautifulSoup
import markdown

def convert_md_inside_html(raw_html):
    raw_html = f"<div>{raw_html}</div>"
    soup = BeautifulSoup(str(raw_html), "html.parser")

    # Choose which tags to scan for embedded Markdown
    for tag in soup.find_all(['p', 'section', 'div']):
        # Convert the text content inside the tag
        html_converted = markdown.markdown(tag.get_text().strip())
        tag.clear()
        tag.append(BeautifulSoup(html_converted, "html.parser"))

    return str(soup)


# temp debugger
def debugger(*args):
    for i, arg in enumerate(args) :
        print(">"*50)
        print(f"Arg num {i}:\n")
        print(arg)


def generate_logs(*args):
    print("\n".join(args))

def fill_email(template_path, template_data):
    """
    Send an HTML email using a Jinja2 template with Markdown rendering.

    Args:
        template_path (str): Path to the HTML template file.
        template_data (dict): Data to render in the template.
    """

    # Add current year & date
    template_data['current_year'] = datetime.datetime.now().year
    template_data['date'] = datetime.datetime.now().strftime('%B %d, %Y')

    try:
        env = Environment(loader=FileSystemLoader(os.path.dirname(template_path)))

        # Register Markdown filter
        env.filters['markdown'] = lambda text: convert_md_inside_html(text)

        # Load the template
        template = env.get_template(os.path.basename(template_path))

        # Render template with Markdown support
        html_content = template.render(**template_data)
        return html_content

    except FileNotFoundError:
        generate_logs("fill_html", "FileNotFound", f"Template file not found: {template_path}")
        return False
    except jinja2.exceptions.TemplateError as e:
        generate_logs("fill_html","jinja2Exception",f"Template rendering error: {e}")
        return False
    except Exception as e:
        generate_logs("fill_html","OtherException",f"Failed to send email: {e}")
        return False

# Generate content with error handling
def get_content_safely(language, template_content, model_name):
    try:
        content = summarize_news(template_content, language, model_name)
        title = generate_title(content,language, model_name)
        return title, content
    except Exception as e:
        print(f"Error generating content: {e}")
        return "Latest Tech News", "<p>Content generation failed. Please check your content generation functions.</p>"

# Main execution
def formHTML(posts):
    current_directory = os.getcwd()

    # Specify your HTML file name or path
    html_folder = "TheNexusModule/html"

    # Combine the current directory with the HTML file path
    html_path = os.path.join(current_directory, html_folder)

    # Generate title and content
    models = ["google/gemma-3-27b-it:free", "google/gemma-3-27b-it:free", "qwen/qwq-32b:free", "qwen/qwq-32b:free"]
    languages = [("Old Classical Arabic",os.path.join(html_path,"template_ar.html"), "ar"), ("Moroccan Dialect in Arabic",os.path.join(html_path,"template_dr.html"), "dr"), ("English",os.path.join(html_path,"template_en.html"), "en"), ("French",os.path.join(html_path,"template_fr.html"), "fr")]

    for i, (lang, path, code) in enumerate(languages):
        time.sleep(5)
        content = ""
        batch_size = 1
        titles = []
        for j in range(0, len(posts), batch_size):
            title, content_part = get_content_safely(lang, posts[j:j + batch_size], models[i])
            content += f"<br>\n<br>\n<br>\n<h1>{title if title.startswith("<strong>") else f"<strong>{title}</strong>"}</h1>\n<br>\n{content_part}"
            titles.append(title)

        content +="<br><br><br><br><br><br><br>"
        for _, source, link in posts:
            content += f"[{source}]({link})"
        debugger(titles, content)
        # Template data with Markdown support
        template_data = {
            'company_name': 'ikhbarIA',
            'title': generate_title("\n".join(titles), lang, models[i]),
            'category': 'Technology',
            'content': content
        }
        # Render email HTML
        html_page = fill_email(
            template_path=path,
            template_data=template_data
        )

        if html_page and "'NoneType' object is not subscriptable" not in html_page:
            with open(os.path.join(html_path, f"generated_{code}.html"), "w") as f:
                f.write(html_page)


if __name__ == "__main__":
    current_directory = os.getcwd()
    with open(os.path.join(current_directory,"TGT.txt"), "r", encoding='utf-8') as file:
                    template_content = file.read()
    posts = [(template_content, "Al Jazeera", "https://www.aljazeera.com/")]
    formHTML(posts)

# title mrewn
# conclusion
# Arabic + latin letters = katrewen
# background colour
