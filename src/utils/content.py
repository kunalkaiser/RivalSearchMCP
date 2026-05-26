"""
Content processing utilities for RivalSearchMCP.
"""

from typing import List

from markdownify import markdownify as _md
from scrapling.parser import Selector

_STRIP_TAGS = ["script", "style", "nav", "footer", "header", "aside", "noscript", "iframe"]


def clean_html_to_markdown(html_content: str, base_url: str = "") -> str:
    if not html_content:
        return ""
    return _md(html_content, strip=_STRIP_TAGS).strip()


def extract_structured_content(html_content: str, base_url: str = "") -> dict:
    if not html_content:
        return {}

    sel = Selector(content=html_content)

    title = ""
    title_el = sel.css_first("title")
    if title_el:
        title = title_el.get_all_text(strip=True)

    description = ""
    meta_el = sel.css_first('meta[name="description"]')
    if meta_el:
        description = meta_el.attrib.get("content", "")

    main_html = html_content
    for css in ("main", '[role="main"]', ".main-content", ".content", "#content", "#main", "body"):
        el = sel.css_first(css)
        if el:
            main_html = str(el)
            break

    return {
        "title": title,
        "description": description,
        "content": clean_html_to_markdown(main_html, base_url),
        "url": base_url,
    }


def format_search_results(results: List[dict]) -> str:
    if not results:
        return "No search results found."

    formatted_parts = []
    for i, result in enumerate(results, 1):
        title = result.get("title", "No title")
        url = result.get("url", "")
        snippet = result.get("snippet", "")
        formatted_parts.append(f"{i}. **{title}**")
        if url:
            formatted_parts.append(f"   URL: {url}")
        if snippet:
            formatted_parts.append(f"   Snippet: {snippet}")
        formatted_parts.append("")

    return " | ".join(formatted_parts)


def format_traversal_results(pages: List[dict]) -> str:
    if not pages:
        return "No pages found."

    formatted_parts = []
    for i, page in enumerate(pages, 1):
        url = page.get("url", "")
        title = page.get("title", "No title")
        content = page.get("content", "")
        depth = page.get("depth", 0)
        indent = "  " * depth
        formatted_parts.append(f"{i}. {indent}**{title}** (depth {depth})")
        if url:
            formatted_parts.append(f"{indent}   URL: {url}")
        if content:
            formatted_parts.append(f"{indent}   Content: {content}")

    return " | ".join(formatted_parts)
