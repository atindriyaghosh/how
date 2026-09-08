"""Build the how bundle (markdown -> static HTML) into dist/."""

from __future__ import annotations

import re
import shutil
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import frontmatter
import mistune
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).parent
BUNDLE_DIR = ROOT / "bundle"
TEMPLATES_DIR = ROOT / "templates"
STATIC_DIR = ROOT / "static"
DIST_DIR = ROOT / "dist"

KNOWN_TYPES = {"principle", "pattern"}
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")


class MermaidRenderer(mistune.HTMLRenderer):
    def block_code(self, code, info=None):
        lang = (info or "").strip().split()[0] if info else ""
        if lang == "mermaid":
            return f'<pre class="mermaid">{mistune.escape(code)}</pre>\n'
        return super().block_code(code, info)


markdown = mistune.create_markdown(renderer=MermaidRenderer())


@dataclass
class Doc:
    slug: str
    path: Path
    type: str
    title: str
    summary: str | None = None
    stack: list[str] = field(default_factory=list)
    app_url: str | None = None
    body: str = ""
    content_html: str = ""


def fail(message: str) -> None:
    print(f"build failed: {message}", file=sys.stderr)
    sys.exit(1)


def load_docs() -> list[Doc]:
    docs = []
    for md_path in sorted(BUNDLE_DIR.rglob("*.md")):
        post = frontmatter.load(md_path)
        doc_type = post.get("type")
        if not doc_type:
            fail(f"{md_path.relative_to(ROOT)}: missing required 'type' field")
        if doc_type not in KNOWN_TYPES:
            fail(
                f"{md_path.relative_to(ROOT)}: unknown type '{doc_type}' "
                f"(known types: {', '.join(sorted(KNOWN_TYPES))})"
            )
        title = post.get("title")
        if not title:
            fail(f"{md_path.relative_to(ROOT)}: missing required 'title' field")

        summary = post.get("summary")
        if not summary:
            fail(f"{md_path.relative_to(ROOT)}: missing required 'summary' field")

        docs.append(
            Doc(
                slug=md_path.stem,
                path=md_path,
                type=doc_type,
                title=title,
                summary=summary,
                stack=post.get("stack") or [],
                app_url=post.get("app_url"),
                body=post.content,
            )
        )
    return docs


def render_bodies(docs: list[Doc]) -> None:
    for doc in docs:
        doc.content_html = markdown(doc.body)


def check_links(docs: list[Doc]) -> None:
    slugs_by_dir = {
        "patterns": {d.slug for d in docs if d.type == "pattern"},
        "principles": {d.slug for d in docs if d.type == "principle"},
    }
    for doc in docs:
        for target in LINK_RE.findall(doc.body):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            match = re.match(r"^(?:\.\./)?(patterns|principles)/([^./]+)(?:\.(?:md|html))?$", target)
            if not match:
                continue
            dir_name, slug = match.groups()
            if slug not in slugs_by_dir[dir_name]:
                fail(
                    f"{doc.path.relative_to(ROOT)}: links to unknown {dir_name[:-1]} "
                    f"slug '{slug}'"
                )


def build() -> None:
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True)

    docs = load_docs()
    render_bodies(docs)
    check_links(docs)

    principles = [d for d in docs if d.type == "principle"]
    patterns = [d for d in docs if d.type == "pattern"]

    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR), autoescape=False)
    year = date.today().year

    index_tmpl = env.get_template("index.html.j2")
    (DIST_DIR / "index.html").write_text(
        index_tmpl.render(root="", year=year, principles=principles, patterns=patterns)
    )

    pattern_tmpl = env.get_template("pattern.html.j2")
    patterns_dir = DIST_DIR / "patterns"
    patterns_dir.mkdir(exist_ok=True)
    for pattern in patterns:
        (patterns_dir / f"{pattern.slug}.html").write_text(
            pattern_tmpl.render(root="../", year=year, pattern=pattern)
        )

    principle_tmpl = env.get_template("principle.html.j2")
    principles_dir = DIST_DIR / "principles"
    principles_dir.mkdir(exist_ok=True)
    for principle in principles:
        (principles_dir / f"{principle.slug}.html").write_text(
            principle_tmpl.render(root="../", year=year, principle=principle)
        )

    for item in STATIC_DIR.iterdir():
        dest = DIST_DIR / item.name
        if item.is_dir():
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)

    print(f"built {len(principles)} principle(s), {len(patterns)} pattern(s) -> dist/")


if __name__ == "__main__":
    build()
