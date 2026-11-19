"""Reproduce the small, reviewed excerpt set from the retained HTML snapshots."""

import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


class Text(HTMLParser):
    """Extract text without fetching images, scripts or linked pages."""

    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


def plain(html):
    parser = Text()
    parser.feed(html)
    return re.sub(r"\s+", " ", "".join(parser.parts)).strip()


def main():
    """Keep paragraph boundaries, source anchors, hashes and required notices."""
    raw = ROOT / "corpus" / "raw"
    specs = [
        (
            "psql",
            "app-psql.html",
            "psql: client-side \\copy",
            "APP-PSQL-META-COMMANDS-COPY",
            'id="APP-PSQL-META-COMMANDS-COPY"',
            '<dt id="APP-PSQL-META-COMMAND-COPYRIGHT"',
            6,
        ),
        (
            "copy",
            "sql-copy.html",
            "COPY: Description",
            "id-1.9.3.55.5",
            "<h2>Description</h2>",
            "<h2>Parameters</h2>",
            5,
        ),
        (
            "json",
            "datatype-json.html",
            "JSON Types: introduction",
            "DATATYPE-JSON",
            "<p>JSON data types",
            "<p>In general",
            4,
        ),
    ]
    records, sources = [], []
    for source_id, page, heading, anchor, start, end, count in specs:
        html = (raw / f"{source_id}.html").read_text()
        section = html[html.index(start) :].split(end)[0]
        paragraphs = re.findall(r"<p\b[^>]*>(.*?)</p>", section, re.S)[:count]
        assert len(paragraphs) == count, f"Snapshot changed: {source_id}"
        url = f"https://www.postgresql.org/docs/18/{page}"
        sources.append(
            {
                "id": source_id,
                "title": heading,
                "url": url,
                "snapshot": f"corpus/raw/{source_id}.html",
                "snapshot_sha256": hashlib.sha256(html.encode()).hexdigest(),
                "fetched_at": "2026-11-19",
                "version": "18",
                "imported_scope": f"{count} paragraphs in {heading}",
                "chunks": count,
            }
        )
        for index, paragraph in enumerate(paragraphs):
            text = plain(paragraph)
            digest = hashlib.sha256(text.encode()).hexdigest()
            records.append(
                {
                    "id": f"pg18-{source_id}-{digest[:16]}",
                    "source_id": source_id,
                    "title": heading,
                    "source_url": f"{url}#{anchor}",
                    "version": "18",
                    "paragraph": index + 1,
                    "text": text,
                    "sha256": digest,
                    "fetched_at": "2026-11-19",
                }
            )
    license_html = (raw / "license.html").read_text()
    license_text = plain(
        license_html.split("PostgreSQL Database Management System", 1)[1].split(
            "<h2>Will PostgreSQL", 1
        )[0]
    )
    license_text = "PostgreSQL Database Management System\n" + license_text
    (ROOT / "corpus" / "LICENSE-PostgreSQL.txt").write_text(license_text + "\n")
    (ROOT / "corpus" / "chunks.json").write_text(json.dumps(records, indent=2) + "\n")
    (ROOT / "corpus" / "sources.json").write_text(json.dumps(sources, indent=2) + "\n")
    print(json.dumps({"sources": len(sources), "chunks": len(records)}))


if __name__ == "__main__":
    main()
