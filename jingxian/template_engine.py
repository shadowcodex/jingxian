# template_engine.py
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from jinja2_time import TimeExtension
from dateutil import parser
from jingxian.markdown_processor import convert_markdown
import base64
from urllib.parse import urlparse, parse_qs

def jinja2_filter_datetime(date, fmt=None):
    native = date.replace(tzinfo=None)
    return native.strftime(fmt) 

def jinja2_filter_markdown(content):
    return convert_markdown(content)

def jinja2_filter_b64decode(value):
    try:
        return base64.b64decode(value).decode()
    except Exception:
        return '[Invalid base64]'

def jinja2_filter_b64encode(value):
    try:
        return base64.b64encode(str(value).encode('utf-8')).decode('utf-8')
    except Exception:
        return '[Encoding error]'

def extract_video_id(url):
    """Extract YouTube video ID from URL."""
    qs = parse_qs(urlparse(url).query)
    return qs.get('v', [''])[0]

def extract_playlist_id(url):
    """Extract YouTube playlist ID from URL."""
    qs = parse_qs(urlparse(url).query)
    return qs.get('list', [''])[0]

def init_template_engine(config, collections, site_path):
    """Initialize Jinja2 environment and set global template variables."""
    templates_path = Path(site_path) / "_templates"
    env = Environment(
        loader=FileSystemLoader(templates_path),
        extensions=[TimeExtension]
    )
    # Inject global context: config and collections data
    env.globals = {**env.globals, **config}
    env.globals["collections"] = collections
    env.filters["strftime"] = jinja2_filter_datetime
    env.filters["markdown"] = jinja2_filter_markdown
    env.filters["b64decode"] = jinja2_filter_b64decode
    env.filters["b64encode"] = jinja2_filter_b64encode
    env.filters['video_id'] = extract_video_id
    env.filters['playlist_id'] = extract_playlist_id
    return env

def render_template(env, template_name, context):
    if template_name:
        template = env.get_template(template_name)
    else:
        from jinja2 import Template
        template = Template(context["raw_markdown"])  # or however you pass it in
    return template.render(context)

