#!/usr/bin/env python3
"""Embed GitHub-rendered paper cards into every archived Markdown report."""

from __future__ import annotations

import argparse
import html
import json
import os
import re
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
DAILY = ROOT / "daily"
ENRICHMENT = ROOT / "data" / "enrichment.json"
START = "<!-- PAPER_CARDS_START -->"
END = "<!-- PAPER_CARDS_END -->"
ARXIV = re.compile(r"https://arxiv\.org/abs/(\d{4}\.\d{4,5})(?:v\d+)?")
MARKDOWN_LINK = re.compile(r"\[([^]]+)\]\([^)]+\)")
CATEGORY_CODE = re.compile(r"\b(?:cs|stat|eess|math|physics|cond-mat)\.[A-Za-z.-]+\b")


def parse_row(line: str) -> dict | None:
    if not line.startswith("|"):
        return None
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    if len(cells) < 8 or not cells[0].isdigit():
        return None
    link_cell = next((i for i in (1, 2) if ARXIV.search(cells[i])), None)
    if link_cell is None:
        return None
    match = ARXIV.search(cells[link_cell])
    offset = 0 if link_cell == 1 else 1
    if len(cells) < 8 + offset:
        return None
    title = MARKDOWN_LINK.sub(lambda item: item.group(1), cells[1]).split(" / PDF")[0].strip()
    if not title:
        return None
    return {
        "rank": int(cells[0]),
        "id": match.group(1),
        "title": title,
        "category": cells[2 + offset],
        "authors": cells[3 + offset],
        "affiliation": cells[4 + offset],
    }


def safe_url(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    parsed = urlparse(value)
    return value if parsed.scheme == "https" and parsed.netloc else None


def inline(value: str) -> str:
    return html.escape(value, quote=False).replace("|", "&#124;").replace("\n", " ")


def image_for(report: Path, paper: dict, extra: dict) -> tuple[str, str]:
    value = extra.get("image")
    image = ROOT / "assets" / "card-placeholder.svg"
    alt = "Paper figure unavailable"
    if isinstance(value, str) and value.startswith("assets/papers/"):
        candidate = ROOT / value
        if candidate.is_file() and candidate.resolve().is_relative_to((ROOT / "assets" / "papers").resolve()):
            image = candidate
            alt = "Paper or project figure"
    return os.path.relpath(image, report.parent).replace(os.sep, "/"), alt


def card(report: Path, paper: dict, enrichment: dict) -> str:
    extra = enrichment.get(paper["id"], {})
    image, alt = image_for(report, paper, extra)
    paper_url = f"https://arxiv.org/abs/{paper['id']}"
    code = CATEGORY_CODE.search(paper["category"])
    category = code.group() if code else paper["category"].split(";")[0][:24]
    venue = extra.get("venue") if isinstance(extra.get("venue"), str) else None
    label = venue or f"arXiv {extra.get('announced_date', report.stem)} · {category}"
    authors = paper["authors"]
    if len(authors) > 125:
        authors = authors[:122].rstrip(" ，,;") + "…"
    links = [f"[Paper]({paper_url})"]
    for name in ("Code", "Project", "Video", "Data"):
        url = safe_url(extra.get(name.lower()))
        if url:
            links.append(f"[{name}]({url})")
    image_source = safe_url(extra.get("image_source"))
    if image_source and alt != "Paper figure unavailable":
        links.append(f"[Figure source]({image_source})")
    abstract_source = safe_url(extra.get("abstract_source"))
    abstract_blocks = []
    for field, abstract_label, missing, source_label in (
        ("abstract_en", "[EN] Abstract", "Original abstract unavailable.", "Source"),
        ("abstract_zh", "[ZH] Abstract", "Chinese translation unavailable.", "Source"),
    ):
        value = extra.get(field)
        abstract = inline(value.strip()) if isinstance(value, str) and value.strip() else missing
        source_link = f'<br><a href="{html.escape(abstract_source, quote=True)}">{source_label}</a>' if abstract_source else ""
        abstract_blocks.append(f"<details><summary>{abstract_label}</summary>{abstract}{source_link}</details>")
    abstract_block = "".join(abstract_blocks)
    return (
        f"![{inline(alt)}]({image})<br>"
        f"<sub>{inline(label)} · #{paper['rank']}</sub><br>"
        f"**[{inline(paper['title'])}]({paper_url})**<br>"
        f"<sub>{inline(authors)}</sub><br>"
        f"<sub>Affiliation: {inline(paper['affiliation'])}</sub><br>"
        + " · ".join(links)
        + "<br>" + abstract_block
    )


def cards_section(report: Path, papers: list[dict], enrichment: dict) -> str:
    rows = []
    for start in range(0, len(papers), 3):
        cells = [card(report, paper, enrichment) for paper in papers[start:start + 3]]
        rows.append("| " + " | ".join(cells + [" "] * (3 - len(cells))) + " |")
    return (
        f"{START}\n## Paper cards\n\n"
        "Cards follow the digest ranking. Expand [EN] for the full original abstract or [ZH] for its complete Chinese translation. Collapse one and expand the other to switch languages independently for each paper. Open the title or Paper link for the original; detailed analysis follows below.\n\n"
        "| Paper | Paper | Paper |\n|---|---|---|\n"
        + "\n".join(rows) + f"\n{END}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", required=True, help="Only rebuild this YYYY-MM-DD report")
    args = parser.parse_args()
    report_path = DAILY / args.date[:4] / f"{args.date}.md"
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.date) or not report_path.is_file():
        parser.error("--date must name an existing daily report")
    enrichment = json.loads(ENRICHMENT.read_text(encoding="utf-8")) if ENRICHMENT.exists() else {}
    reports = 0
    cards = 0
    for report in [report_path]:
        source = report.read_text(encoding="utf-8")
        body = source
        if START in body:
            body = re.sub(rf"{re.escape(START)}.*?{re.escape(END)}\n*", "", body, count=1, flags=re.S)
        papers = []
        seen = set()
        for line in body.splitlines():
            paper = parse_row(line)
            if paper and paper["id"] not in seen:
                papers.append(paper)
                seen.add(paper["id"])
        if not papers:
            if source != body:
                report.write_text(body, encoding="utf-8")
            continue
        lines = body.splitlines(keepends=True)
        first_heading = next((i for i, line in enumerate(lines) if line.startswith("# ")), None)
        position = first_heading + 1 if first_heading is not None else 0
        insertion = "\n" + cards_section(report, papers, enrichment) + "\n\n"
        output = "".join(lines[:position]) + insertion + "".join(lines[position:]).lstrip("\n")
        if output != source:
            report.write_text(output, encoding="utf-8")
        reports += 1
        cards += len(papers)
    print(f"Embedded {cards} cards in {reports} Markdown reports")


if __name__ == "__main__":
    main()
