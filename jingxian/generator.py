# generator.py
import os, shutil, json, glob, textwrap
from pathlib import Path
from jingxian.content_parser import parse_content
from jingxian.markdown_processor import convert_markdown
from jingxian.template_engine import init_template_engine, render_template
from jingxian.logger import get_logger
from datetime import datetime

logger = get_logger("generator")

def build_site(site_path):

    # 1. Load configuration
    with open(Path.joinpath(site_path, "config.json")) as cfg:
        config = json.load(cfg)
    output_dir = Path.joinpath(site_path, config.get("output_dir", "output"))
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    logger.info("Loaded configuration")
    
    # 2. Load collections data (global JSON data for templates)
    collections_data = {}
    for coll_file in Path(Path.joinpath(site_path, "collections")).glob("*.json"):
        name = coll_file.stem  # filename without extension
        with open(coll_file) as f:
            collections_data[name] = json.load(f)
    logger.info(f"Loaded collections: {list(collections_data.keys())}")

    # --- Load extra configs
    config['site']['time'] = datetime.now()
    
    # 3. Initialize template engine with config and collections
    template_env = init_template_engine(config, collections_data, site_path)

    # 5. Process Data-Driven Pages from JSON data
    data_file_pages = {}
    for data_file in Path(Path.joinpath(site_path,"_datapages")).glob("*.json"):
        logger.info(f"datafile: {data_file}")
        name = data_file.stem  # e.g. "projects" for projects.json
        pages_in_file = []
        with open(data_file) as f:
            data = json.load(f)
            logger.info(data)
        # Use a template matching the data file name (e.g. projects.html)
            for page in data:
                logger.info(page)
                template_name = f"{name}.html"
                context = {
                    "page": page['page'],
                    "data": page
                }
                # Render page (or pages) using the data. 
                # For simplicity, generate a single page per data file:
                output_path = Path(output_dir) / name / page['page']['slug'] / "index.html"
                output_path.parent.mkdir(parents=True, exist_ok=True)
                html = render_template(template_env, template_name, context)
                output_path.write_text(html)
                pages_in_file.append(page['page']['slug'])
                logger.info(f"Generated data-driven page: {output_path}")
        # (Optionally, if the JSON is a list of items and individual pages per item are needed,
        # you could iterate and render multiple pages here.)
        data_file_pages[name] = pages_in_file

    # 4. Process Markdown articles
    for md_file in Path(Path.joinpath(site_path,"_content/articles")).rglob("*.md"):
        front_matter, md_content = parse_content(md_file)

        # Render the raw markdown through Jinja first
        template = template_env.from_string(md_content)
        rendered_md = template.render({
            "datapages": data_file_pages,
            "page": front_matter,
        })

        # Then convert to HTML
        html_content = convert_markdown(textwrap.dedent(rendered_md))
        template_name = front_matter.get("template", "page") + ".html"
        context = {
            "page": front_matter,
            "content": html_content,
            "datapages": data_file_pages
        }
        output_path = Path(output_dir) / "articles" / md_file.stem / "index.html"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        html = render_template(template_env, template_name, context)
        output_path.write_text(html)
        logger.info(f"Generated article: {output_path}")
    
    # 6. Process Markdown pages (standalone)
    for md_file in Path(Path.joinpath(site_path,"_content/pages")).rglob("*.md"):
        front_matter, md_content = parse_content(md_file)

        # Render the raw markdown through Jinja first
        template = template_env.from_string(md_content)
        rendered_md = template.render({
            "datapages": data_file_pages,
            "page": front_matter,
        })

        # Then convert to HTML
        html_content = convert_markdown(textwrap.dedent(rendered_md))
        template_name = front_matter.get("template", "page") + ".html"
        context = {
            "page": front_matter,
            "content": html_content,
            "datapages": data_file_pages
        }

        # Output as /<pagename>/index.html for clean URLs
        output_path = Path(output_dir) / md_file.stem / "index.html"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        html = render_template(template_env, template_name, context)
        # print(html)
        try:
            output_path.write_text(html, encoding='utf-8')
        except Exception as e:
            logger.error(f"❌ Failed to write {output_path}: {e}")

        logger.info(f"Generated page: {output_path}")
    
    
    
    # 7. Copy static assets to output
    static_src = Path(Path.joinpath(site_path,"_static"))
    static_dest = Path(output_dir) / "static"
    if static_src.exists():
        shutil.copytree(static_src, static_dest, dirs_exist_ok=True)
        logger.info("Copied static assets")
    
    logger.info("Site generation complete.")

# If executed directly, build the site
if __name__ == "__main__":
    build_site()
