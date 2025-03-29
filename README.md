# jingxian (经线) (Jīngxiàn) - "Meridian" - A python static side generator.

Jīngxiàn (经线) – "Meridian" is a static site generator built with a focus on data-driven content generation. Unlike traditional static site generators that primarily process Markdown files, Jīngxiàn is designed to transform structured JSON data—whether stored in files or sourced from a backend—into fully rendered, static HTML pages. The name Jīngxiàn reflects this philosophy: in Chinese, Jīngxiàn refers to both geographical meridians that structure the world and qì meridians in traditional Chinese medicine that channel energy through the body. In the same way, Jīngxiàn acts as the structured path through which data flows, transforming raw content into an organized, navigable website. By prioritizing simplicity and clarity, it makes working with structured data effortless—whether you're building educational resources, knowledge bases, or any site where dynamically generated static pages are key.

*Jīngxiàn* is designed to be accessible to **non-engineers**, making it easy for designers and content creators to build dynamic, data-driven sites without needing deep programming knowledge. If you're comfortable with **design systems, basic data structures, and Markdown**, you can use *Jīngxiàn* to create powerful static websites effortlessly. The goal is to remove unnecessary complexity, allowing users to focus on content and design while the generator handles the structured transformation of data into a fully functional site.

## Why?

I decided to build my own static site generator because I found a lack of support for truly **data-driven** static site generators—especially ones that are **straightforward and simple** to use. Many existing solutions either focus solely on Markdown-based content or make working with structured data unnecessarily complex. *Jīngxiàn* is designed specifically to address this gap by making **data-driven page generation** a first-class feature. Its core use case is taking JSON-based data—whether from a simple file or derived from a backend/database—and transforming it into static pages that can be efficiently served via platforms like GitHub Pages. Just as meridians channel *qì* smoothly through the body, *Jīngxiàn* provides a structured yet flexible flow of data into well-organized static sites, making dynamic content generation as seamless as possible.

## Dev Process

Install locally:

```
poetry run pip install --editable .
```

Usage:
```
jingxian build <path>
jingxian serve <path>
```

## Expected Folder structure.
```
hanzi-v2/
├── _collections/            # JSON collections reusable across all pages (e.g. authors, metadata)
├── _content/                # Markdown-driven content for articles and pages
│   ├── articles/
│   └── pages/
├── _data/                   # General-purpose JSON data used inside templates/
├── _datapages/              # JSON arrays used to generate data-driven pages (one page per entry)
├── _static/                 # Static assets to be copied directly (CSS, images, JS, etc.)
│   ├── css/
│   │   └── styles.css
├── _templates/              # Jinja2 templates for layouts and pages
│   ├── includes/            # Reusable partials (e.g., header, footer)
│   ├── base.html            # Base layout extended by other templates
│   ├── index.html           # Homepage template
├── scripts/                 # Utility scripts (build helpers, data transformers, etc.)
├── config.json              # Global site configuration and data-driven page setup
```