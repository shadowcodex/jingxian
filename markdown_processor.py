# markdown_processor.py
import markdown

def convert_markdown(markdown_text):
    """Convert Markdown text to HTML string."""
    html = markdown.markdown(markdown_text)
    return html
