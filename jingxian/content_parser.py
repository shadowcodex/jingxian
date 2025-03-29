# content_parser.py
import json
from pathlib import Path

def parse_content(file_path):
    """Parse a Markdown file into front matter (dict) and content (Markdown string)."""
    text = Path(file_path).read_text(encoding="utf-8")
    front_matter = {}
    content = text
    # Identify JSON front matter if present at the top of the file
    if text.strip().startswith("{"):
        # Find the delimiter line indicating end of JSON front matter
        delimiter_index = text.find("\n---")
        if delimiter_index != -1:
            json_text = text[:delimiter_index]
            try:
                front_matter = json.loads(json_text)
            except json.JSONDecodeError as e:
                # If JSON is malformed, log an error (using logger) and continue with empty front_matter
                print(f"Front matter JSON parse error in {file_path}: {e}")
                front_matter = {}
            # The rest after the delimiter is the Markdown content
            content = text[delimiter_index + 4:]  # skip over "\n---"
        else:
            # No delimiter found, treat whole text as content (no front matter)
            content = text
    else:
        # If it doesn't start with '{', assume no front matter
        content = text
    # Strip leading/trailing whitespace from content
    content = content.lstrip()  
    return front_matter, content
