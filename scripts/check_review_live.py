"""Save real HTTPS import/query/link evidence; never use model credentials."""

from datetime import datetime, timezone
from html.parser import HTMLParser
import json
from pathlib import Path
import ssl
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen

import certifi

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://shiv-is373.xyz"
OUT = ROOT / "docs/review-2"


class Links(HTMLParser):
    """Inspect the actual links the server returns, including fragments."""

    def __init__(self):
        super().__init__()
        self.links, self.ids = [], set()

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "id" in values:
            self.ids.add(values["id"])
        if tag == "a" and values.get("href"):
            self.links.append(values["href"])


def request(path, body=None):
    """HTTPS verification stays on; capture only public application data."""
    url = urljoin(ORIGIN, path)
    data = json.dumps(body).encode() if body is not None else None
    req = Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "IS373-review-check/1.0",
        },
    )
    with urlopen(
        req, timeout=25, context=ssl.create_default_context(cafile=certifi.where())
    ) as response:
        text = response.read().decode()
        return response.status, text, response.url


def main():
    """Check the deployed app, its real traces, and every portfolio link."""
    evidence = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "origin": ORIGIN,
        "tls_verification": True,
        "routes": [],
        "links": [],
        "query_traces": [],
    }
    pages = {}
    for path in (
        "/portfolio",
        "/portfolio/rag",
        "/portfolio/delivery",
        "/rag",
        "/review-static/review.css",
        "/review-static/rag.js",
        "/api/review/sources",
        "/api/review/license",
    ):
        status, text, final = request(path)
        evidence["routes"].append({"path": path, "status": status, "final_url": final})
        assert status == 200
        if path.startswith("/portfolio"):
            pages[path] = text
    ids = ["psql", "copy", "json"]
    imports = []
    for _ in range(2):
        _, text, _ = request("/api/review/import", {"source_ids": ids})
        imports.append(json.loads(text))
    assert imports[0]["chunk_ids"] == imports[1]["chunk_ids"]
    assert imports[1]["inserted"] == 0
    assert imports[1]["total_chunks"] == 15
    evidence["imports"] = imports
    (OUT / "sample-representation.json").write_text(
        json.dumps(imports[0]["sample"], indent=2) + "\n"
    )
    questions = [
        "Can I import a CSV from my laptop if PostgreSQL runs on a different machine?",
        "Who reads the file for SQL COPY FROM 'file.csv' versus psql \\copy?",
        "How does jsonb differ from json?",
        "What is the password for my database?",
    ]
    for question in questions:
        _, text, _ = request(
            "/api/review/query", {"question": question, "source_ids": ids}
        )
        trace = json.loads(text)
        evidence["query_traces"].append(trace)
    first, comparison, json_trace, unsupported = evidence["query_traces"]
    assert "frontend (client) copy" in first["answer"]
    assert "server to directly read" in comparison["answer"]
    assert "frontend (client) copy" in comparison["answer"]
    assert "decomposed binary format" in json_trace["answer"]
    assert unsupported["status"] == "insufficient_evidence"
    assert unsupported["sources"] == []
    (OUT / "query-answer-trace.json").write_text(json.dumps(first, indent=2) + "\n")
    seen = set()
    for trace in evidence["query_traces"]:
        for source in trace["sources"]:
            pages.setdefault(
                source["url"], '<a href="' + source["url"] + '">Citation</a>'
            )
    for path, html in pages.items():
        parser = Links()
        parser.feed(html)
        for href in parser.links:
            url = urljoin(ORIGIN + path, href)
            if url in seen:
                continue
            seen.add(url)
            try:
                status, destination, final = request(url)
                result = {"url": url, "status": status, "final_url": final}
                fragment = urlsplit(url).fragment
                if fragment:
                    parsed = Links()
                    parsed.feed(destination)
                    result["fragment_present"] = (
                        fragment in parsed.ids
                        or ("user-content-" + fragment) in parsed.ids
                    )
                evidence["links"].append(result)
            except Exception as error:  # Preserve a failed check; never call it passed.
                evidence["links"].append({"url": url, "error": str(error)})
    for url in (ORIGIN, "https://qa.shiv-is373.xyz", "https://calc.shiv-is373.xyz"):
        status, _, final = request(url)
        evidence.setdefault("existing_projects", []).append(
            {"url": url, "status": status, "final_url": final}
        )
    (OUT / "live-checks.json").write_text(json.dumps(evidence, indent=2) + "\n")
    print(
        json.dumps(
            {
                "routes": len(evidence["routes"]),
                "queries": len(questions),
                "repeat_import_inserted": imports[1]["inserted"],
                "links": evidence["links"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
