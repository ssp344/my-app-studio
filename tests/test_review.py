"""Exercise real import, provenance, ranking and refusal boundaries."""

import hashlib


def test_import_is_idempotent_and_metadata_matches_snapshot(client):
    """Repeated import reuses IDs, with real text and resolvable versioned provenance."""
    payload = {"source_ids": ["psql", "copy", "json"]}
    first = client.post("/api/review/import", json=payload).json()
    second = client.post("/api/review/import", json=payload).json()
    assert first["inserted"] == first["selected_chunks"] == 15
    assert second["inserted"] == 0
    assert first["chunk_ids"] == second["chunk_ids"]
    assert second["total_chunks"] == 15
    sample = second["sample"]
    assert sample["sha256"] == hashlib.sha256(sample["text"].encode()).hexdigest()
    assert sample["version"] == "18"
    assert sample["source_url"].endswith("#APP-PSQL-META-COMMANDS-COPY")
    assert "Permission to use, copy" in client.get(first["license_url"]).text


def test_question_traces_and_unknown_question(client):
    """Actual retrieval supports planned questions; no password is invented."""
    ids = ["psql", "copy", "json"]
    client.post("/api/review/import", json={"source_ids": ids})
    questions = [
        (
            "Can I import a CSV from my laptop if PostgreSQL runs on a different machine?",
            "psql",
        ),
        ("Who reads the file for SQL COPY FROM 'file.csv' versus psql \\copy?", "copy"),
        ("How does jsonb differ from json?", "json"),
    ]
    for question, expected_source in questions:
        response = client.post(
            "/api/review/query", json={"source_ids": ids, "question": question}
        )
        assert response.status_code == 200
        trace = response.json()
        assert expected_source in {item["source_id"] for item in trace["retrieved"]}
        assert trace["sources"]
        if "versus" in question:
            assert len(trace["sources"]) == 2
            assert "server to directly read" in trace["answer"]
            assert "frontend (client) copy" in trace["answer"]
        for citation in trace["sources"]:
            passage = next(
                item
                for item in trace["retrieved"]
                if item["id"] == citation["chunk_id"]
            )
            assert passage["text"] in trace["answer"]
            assert passage["source_url"] == citation["url"]
    unknown = client.post(
        "/api/review/query",
        json={"source_ids": ids, "question": "What is the password for my database?"},
    ).json()
    assert unknown["status"] == "insufficient_evidence"
    assert unknown["sources"] == []


def test_source_scope_validation_and_import_required(client):
    """Never fetch caller URLs or silently search unselected/unimported sources."""
    assert (
        client.post(
            "/api/review/import", json={"source_ids": ["https://example.com"]}
        ).status_code
        == 422
    )
    assert client.post("/api/review/import", json={"source_ids": []}).status_code == 422
    payload = {"source_ids": ["json"], "question": "How does jsonb differ from json?"}
    assert client.post("/api/review/query", json=payload).status_code == 409
    client.post("/api/review/import", json={"source_ids": ["json"]})
    trace = client.post("/api/review/query", json=payload).json()
    assert all(item["source_id"] == "json" for item in trace["retrieved"])
    payload["question"] = "x" * 501
    assert client.post("/api/review/query", json=payload).status_code == 422


def test_portfolio_routes_and_existing_bookstore(client):
    """New review pages coexist with the earlier application routes."""
    for path in ("/portfolio", "/portfolio/rag", "/portfolio/delivery", "/rag"):
        assert client.get(path).status_code == 200
    assert client.get("/portfolio/unknown").status_code == 404
    assert "Book Store" in client.get("/").text
    assert client.get("/review-static/review.css").status_code == 200
