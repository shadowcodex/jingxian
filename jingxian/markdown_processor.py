# markdown_processor.py
from markdown_it import MarkdownIt

def convert_markdown(markdown_text):
    md = MarkdownIt("commonmark", {"html": True})
    return md.render(markdown_text)