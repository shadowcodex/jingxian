# template_engine.py
from jinja2 import Environment, FileSystemLoader

def init_template_engine(config, collections):
    """Initialize Jinja2 environment and set global template variables."""
    env = Environment(loader=FileSystemLoader("templates"))
    # Inject global context: config and collections data
    env.globals["config"] = config
    for name, data in collections.items():
        env.globals[name] = data
    return env

def render_template(env, template_name, context):
    """Render a template with the given context dict using the provided Jinja2 environment."""
    template = env.get_template(template_name)
    return template.render(**context)
