"""Individual portfolio and a bounded, no-key document question-answering app."""

from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import re
import sqlite3

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field

router = APIRouter()
CORPUS = Path(__file__).resolve().parents[2] / "corpus"
STOP = set(
    "a an the to of for is are does do can i my if on from in and or "
    "what how who it this that with as be by me into versus different "
    "between when has have your please tell about".split()
)
EXPANSIONS = {
    "laptop": "local client",
    "remote": "server",
    "import": "copy",
    "csv": "copy file",
    "reads": "read",
    "reading": "read",
    "stores": "store",
    "differs": "difference",
    "differ": "difference",
}


def tokens(text, expand=False):
    """Retain the distinction between the literal commands COPY and backslash-copy."""
    terms = re.findall(r"\\copy|[a-z0-9]+", text.lower())
    result = [term for term in terms if term not in STOP]
    if expand:
        for term in terms:
            result.extend(EXPANSIONS.get(term, "").split())
    return result


def connect(request):
    """The corpus database is separate from existing account data."""
    path = request.app.state.settings.database.with_name("review-corpus.sqlite3")
    connection = sqlite3.connect(path, timeout=5)
    connection.execute(
        "CREATE TABLE IF NOT EXISTS chunks "
        "(id TEXT PRIMARY KEY, source_id TEXT NOT NULL, record TEXT NOT NULL)"
    )
    return connection


class ImportBody(BaseModel):
    """Only the three reviewed snapshots can be imported; no arbitrary URL fetching."""

    source_ids: list[str] = Field(min_length=1, max_length=3)


class QueryBody(ImportBody):
    """Bound query length and use each visitor's selected source set."""

    question: str = Field(min_length=3, max_length=500)


def validate_sources(source_ids):
    """Validate every source before any import side effects."""
    if not set(source_ids) <= {"psql", "copy", "json"}:
        raise HTTPException(422, "Choose only the permitted PostgreSQL snapshots.")


def retrieve(question, records):
    """Exact sparse TF-IDF cosine ranking; no remote service or learned embeddings."""
    documents = [tokens(record["title"] + " " + record["text"]) for record in records]
    frequencies = Counter(term for doc in documents for term in set(doc))
    idf = {
        term: math.log((1 + len(documents)) / (1 + count)) + 1
        for term, count in frequencies.items()
    }

    def vector(terms):
        counts = Counter(term for term in terms if term in idf)
        values = {
            term: (1 + math.log(count)) * idf[term] for term, count in counts.items()
        }
        norm = math.sqrt(sum(value * value for value in values.values())) or 1
        return {term: value / norm for term, value in values.items()}

    query_vector = vector(tokens(question, expand=True))
    ranked = []
    for record, terms in zip(records, documents):
        score = sum(
            value * query_vector.get(term, 0) for term, value in vector(terms).items()
        )
        if score >= 0.10:
            ranked.append({**record, "score": round(score, 6)})
    return sorted(ranked, key=lambda item: (-item["score"], item["id"]))[:5]


@router.get("/portfolio", include_in_schema=False)
@router.get("/portfolio/{case}", include_in_schema=False)
def portfolio(request: Request, case: str = "index"):
    """Keep stable case-study URLs while leaving the bookstore homepage intact."""
    if case not in {"index", "rag", "delivery"}:
        raise HTTPException(404)
    return request.app.state.templates.TemplateResponse(
        request=request, name="portfolio.html", context={"case": case}
    )


@router.get("/rag", include_in_schema=False)
def rag_page(request: Request):
    """A public reviewer demo without account creation."""
    return request.app.state.templates.TemplateResponse(
        request=request, name="rag.html", context={}
    )


@router.get("/api/review/sources")
def sources():
    """Publish the permitted import manifest, never host credentials."""
    return {
        "sources": json.loads((CORPUS / "sources.json").read_text()),
        "mode": "extractive",
        "license_url": "/api/review/license",
    }


@router.get("/api/review/license", response_class=PlainTextResponse)
def license_notice():
    """Retain the required notices alongside distributed excerpts."""
    return (CORPUS / "LICENSE-PostgreSQL.txt").read_text()


@router.post("/api/review/import")
def import_sources(body: ImportBody, request: Request):
    """Idempotently import approved snapshot excerpts with content-derived IDs."""
    validate_sources(body.source_ids)
    selected = [
        record
        for record in json.loads((CORPUS / "chunks.json").read_text())
        if record["source_id"] in body.source_ids
    ]
    with connect(request) as connection:
        before = connection.execute("SELECT count(*) FROM chunks").fetchone()[0]
        connection.executemany(
            "INSERT OR IGNORE INTO chunks VALUES (?, ?, ?)",
            [(item["id"], item["source_id"], json.dumps(item)) for item in selected],
        )
        after = connection.execute("SELECT count(*) FROM chunks").fetchone()[0]
    return {
        "selected_chunks": len(selected),
        "inserted": after - before,
        "total_chunks": after,
        "chunk_ids": sorted(item["id"] for item in selected),
        "sample": selected[0],
        "license_url": "/api/review/license",
    }


@router.post("/api/review/query")
def query(body: QueryBody, request: Request):
    """Compose an extractive answer only from retrieved text, exposing its trace."""
    validate_sources(body.source_ids)
    with connect(request) as connection:
        records = [
            json.loads(row[0])
            for row in connection.execute("SELECT record FROM chunks")
        ]
    records = [item for item in records if item["source_id"] in body.source_ids]
    if not records:
        raise HTTPException(409, "Import the selected source snapshots first.")
    passages = retrieve(body.question, records)
    # Corpus overlap alone cannot establish an answer to every question. This
    # narrow demonstration declines questions without its explicit topic terms.
    topic = set(tokens(body.question, expand=True)) & {
        "copy",
        "\\copy",
        "json",
        "jsonb",
    }
    supported = bool(passages and topic)
    citations = []
    if supported:
        # Prefer evidence from distinct manuals for command-comparison questions.
        seen = set()
        for passage in passages:
            if passage["source_id"] not in seen:
                citations.append(passage)
                seen.add(passage["source_id"])
            if len(citations) == 2:
                break
    answer = (
        "\n\n".join(
            f"[{index}] {item['text']}" for index, item in enumerate(citations, 1)
        )
        if supported
        else "Insufficient evidence in the selected imported excerpts. "
        "Try a question about PostgreSQL COPY, psql \\copy, or json/jsonb."
    )
    return {
        "question": body.question,
        "mode": "extractive (no generative model)",
        "status": "supported_excerpt" if supported else "insufficient_evidence",
        "answer": answer,
        "retrieved": passages,
        "sources": [
            {
                "citation": index,
                "chunk_id": item["id"],
                "url": item["source_url"],
                "title": item["title"],
            }
            for index, item in enumerate(citations, 1)
        ],
        "corpus_digest": hashlib.sha256(
            "".join(sorted(item["id"] for item in records)).encode()
        ).hexdigest(),
    }
