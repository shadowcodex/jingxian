# generator.py
import os, shutil, json, glob
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
    
    # 4. Process Markdown articles
    for md_file in Path(Path.joinpath(site_path,"_content/articles")).rglob("*.md"):
        front_matter, md_content = parse_content(md_file)
        html_content = convert_markdown(md_content)  # Markdown -> HTML&#8203;:contentReference[oaicite:0]{index=0}
        # Determine template to use: from front matter or default
        template_name = front_matter.get("template", "article.html")
        # Combine context: front matter fields + rendered HTML content
        context = {"page": front_matter, "content": html_content}
        output_path = Path(output_dir) / "articles" / md_file.stem / "index.html"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        html = render_template(template_env, template_name, context)
        output_path.write_text(html)
        logger.info(f"Generated article: {output_path}")
    
    # 5. Process Markdown pages (standalone)
    for md_file in Path(Path.joinpath(site_path,"_content/pages")).rglob("*.md"):
        front_matter, md_content = parse_content(md_file)
        html_content = convert_markdown(md_content)
        template_name = front_matter.get("template", "page.html")
        context = {"page": front_matter, "content": html_content}
        # Output as /<pagename>/index.html for clean URLs
        output_path = Path(output_dir) / md_file.stem / "index.html"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        html = render_template(template_env, template_name, context)
        output_path.write_text(html)
        logger.info(f"Generated page: {output_path}")
    
    # 6. Process Data-Driven Pages from JSON data
    for data_file in Path(Path.joinpath(site_path,"_datapages")).glob("*.json"):
        name = data_file.stem  # e.g. "projects" for projects.json
        with open(data_file) as f:
            data = json.load(f)
        # Use a template matching the data file name (e.g. projects.html)
        template_name = f"{name}.html"
        context = {"data": data}
        # Render page (or pages) using the data. 
        # For simplicity, generate a single page per data file:
        output_path = Path(output_dir) / name / "index.html"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        html = render_template(template_env, template_name, context)
        output_path.write_text(html)
        logger.info(f"Generated data-driven page: {output_path}")
        # (Optionally, if the JSON is a list of items and individual pages per item are needed,
        # you could iterate and render multiple pages here.)
    
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
