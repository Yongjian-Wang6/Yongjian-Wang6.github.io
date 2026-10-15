#!/usr/bin/env python3
"""Validate public content, generated files, links, and publication states."""
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []
        self.papers = {}
        self.broken_classes = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        for key in ("href", "src"):
            if attrs.get(key):
                self.links.append(attrs[key])
        if tag == "article" and "data-status" in attrs:
            self.papers[attrs["id"]] = attrs["data-status"]
        self.broken_classes.extend(key for key in attrs if key == "class-")


def main():
    data = json.loads((DOCS / "data/profile.json").read_text())
    page = Page()
    page.feed((DOCS / "index.html").read_text())
    assert len(page.ids) == len(set(page.ids)), "Duplicate page anchors"
    assert not page.broken_classes, "Invalid generated class attribute"
    for link in page.links:
        if link.startswith("#"):
            assert link[1:] in page.ids, f"Missing anchor: {link}"
        elif not urlparse(link).scheme:
            assert (DOCS / unquote(link)).is_file(), f"Missing resource: {link}"
        else:
            assert urlparse(link).scheme in {"https", "mailto"}, f"Unexpected link: {link}"
    papers = data["papers"]
    assert len(page.papers) == len(papers)
    assert len({p["id"] for p in papers}) == len(papers)
    for p in papers:
        assert p["status"] in {"published", "under-review", "withdrawn"}
        assert page.papers["paper-" + p["id"]] == p["status"]
        assert data["name"] in p["authors"] or data["name_zh"] in p["authors"]
        assert p["source"]
    withdrawn = next(p for p in papers if p["id"] == "functional-barriers")
    assert withdrawn["status"] == "withdrawn"
    assert "planned" in withdrawn["note"]["en"]
    assert "arxiv.org" not in withdrawn.get("url", ""), "Only add arXiv after release"
    # Check rendered public material and the content source, rather than embedding
    # private terms in a publicly committed test fixture.
    for path in [DOCS / "index.html", DOCS / "data/profile.json", *sorted((ROOT / "profile").glob("*.md"))]:
        text = path.read_text()
        assert not re.search(r"(?<!\d)1[3-9]\d{9}(?!\d)", text), f"Phone-like number in {path}"
        assert not re.search(r"本科|Bachelor|B\.Sc\.", text, re.I), f"Unexpected education in {path}"
    assert not list(DOCS.rglob("*.pdf")), "Original CV must not be published"
    assert (ROOT / "profile/README.md").is_file()
    print(f"PASS: {len(papers)} papers, {len(page.ids)} unique anchors, all local assets and public-content checks")


if __name__ == "__main__":
    main()
