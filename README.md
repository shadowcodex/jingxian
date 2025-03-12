# jingxian (经线) (Jīngxiàn) - "Meridian" - A python static side generator.

Jīngxiàn (经线) – "Meridian" is a static site generator built with a focus on data-driven content generation. Unlike traditional static site generators that primarily process Markdown files, Jīngxiàn is designed to transform structured JSON data—whether stored in files or sourced from a backend—into fully rendered, static HTML pages. The name Jīngxiàn reflects this philosophy: in Chinese, Jīngxiàn refers to both geographical meridians that structure the world and qì meridians in traditional Chinese medicine that channel energy through the body. In the same way, Jīngxiàn acts as the structured path through which data flows, transforming raw content into an organized, navigable website. By prioritizing simplicity and clarity, it makes working with structured data effortless—whether you're building educational resources, knowledge bases, or any site where dynamically generated static pages are key.

*Jīngxiàn* is designed to be accessible to **non-engineers**, making it easy for designers and content creators to build dynamic, data-driven sites without needing deep programming knowledge. If you're comfortable with **design systems, basic data structures, and Markdown**, you can use *Jīngxiàn* to create powerful static websites effortlessly. The goal is to remove unnecessary complexity, allowing users to focus on content and design while the generator handles the structured transformation of data into a fully functional site.

## Why?

I decided to build my own static site generator because I found a lack of support for truly **data-driven** static site generators—especially ones that are **straightforward and simple** to use. Many existing solutions either focus solely on Markdown-based content or make working with structured data unnecessarily complex. *Jīngxiàn* is designed specifically to address this gap by making **data-driven page generation** a first-class feature. Its core use case is taking JSON-based data—whether from a simple file or derived from a backend/database—and transforming it into static pages that can be efficiently served via platforms like GitHub Pages. Just as meridians channel *qì* smoothly through the body, *Jīngxiàn* provides a structured yet flexible flow of data into well-organized static sites, making dynamic content generation as seamless as possible.

## Dev Process

I am going to start with building basic functionality to use directly, and eventually leverage this to build a repeatable tool that others can use to build their websites.


I hope to have a basic set of functions such as:

- `poetry run build`
- `poetry run serve`

etc...