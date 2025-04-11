# template_engine.py
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from jinja2_time import TimeExtension
from dateutil import parser
from jingxian.markdown_processor import convert_markdown

def jinja2_filter_datetime(date, fmt=None):
    native = date.replace(tzinfo=None)
    return native.strftime(fmt) 

def jinja2_filter_markdown(content):
    return convert_markdown(content)

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
    return env

def render_template(env, template_name, context):
    if template_name:
        template = env.get_template(template_name)
    else:
        from jinja2 import Template
        template = Template(context["raw_markdown"])  # or however you pass it in
    return template.render(context)

