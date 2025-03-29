# template_engine.py
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from jinja2_time import TimeExtension
from dateutil import parser

def jinja2_filter_datetime(date, fmt=None):
    native = date.replace(tzinfo=None)
    return native.strftime(fmt) 

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
    return env

def render_template(env, template_name, context):
    """Render a template with the given context dict using the provided Jinja2 environment."""
    template = env.get_template(template_name)
    return template.render(**context)
