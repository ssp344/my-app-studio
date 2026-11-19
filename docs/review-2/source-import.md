# PostgreSQL 18 source/import record

This is build evidence for the existing [individual review record](https://github.com/ssp344/IS-373/blob/review-2-build/IS373-Individual-Plan.md#review-2-build), not a second review report.

Fetched November 19, 2026 from the original PostgreSQL website. Full HTML snapshots are retained in [corpus/raw](../../corpus/raw), but **only 15 selected paragraphs are imported/indexed**, not the entire manuals. The UI imports any selected subset of these three sources into SQLite. It does not fetch caller-supplied URLs, upload files, or import private content.

| Original source | Actual imported scope | Count |
| --- | --- | --- |
| [psql](https://www.postgresql.org/docs/18/app-psql.html#APP-PSQL-META-COMMANDS-COPY) | Six paragraphs in the `\copy` entry, including client-side file access and the two tips | 6 |
| [SQL COPY](https://www.postgresql.org/docs/18/sql-copy.html#id-1.9.3.55.5) | Five paragraphs in Description: table/file transfer, columns, server file access, progress, and error behavior | 5 |
| [JSON Types](https://www.postgresql.org/docs/18/datatype-json.html#DATATYPE-JSON) | First four introduction paragraphs: valid JSON, available types, efficiency/indexing, preservation of text/keys | 4 |

The [PostgreSQL License](https://www.postgresql.org/about/licence/) expressly permits copying the software and documentation with its required notices. The complete [copyright, permission and disclaimers](../../corpus/LICENSE-PostgreSQL.txt) accompany the snapshots and excerpts and are linked beside the displayed material in the app.

[Source manifest](../../corpus/sources.json) records page URLs, fetch date, version, exact scope and snapshot SHA-256. [Reproducible extraction script](../../scripts/prepare_corpus.py) reads the retained snapshots without network access and preserves paragraph boundaries. Its assertions stop if the expected paragraph count changes. [Extracted chunks](../../corpus/chunks.json) retain content-derived stable IDs, text hashes, source anchors, version and paragraph ordinals. Full snapshots retain navigation; navigation is not indexed.

## Stored representation and retrieval

The [sample representation](sample-representation.json) is a real row returned by the live importer. SQLite stores `id`, `source_id`, and the complete JSON chunk in a `chunks` table, in a dedicated persisted corpus database separate from account data. Identical imports use `INSERT OR IGNORE` against the stable ID. The real repeat-import output is in [live checks](live-checks.json).

At query time, the app tokenizes the selected imported chunks and computes sparse TF-IDF vectors (log term frequency; smoothed inverse document frequency; unit normalization). It performs exact cosine ranking and returns up to five passages scoring at least 0.10. The vector coordinates are computed on demand, not stored as learned embeddings. [Vocabulary expansion](../../app/features/review.py) maps a few explicit terms such as `laptop` to `local client` and `import` to `copy`; this is hand-authored lexical matching, not semantic model inference. Each answer quotes the strongest passage from up to two distinct sources and resolves its stored chunk ID to the original URL.

## Technical research and departure from Review 1

The plan compared exact vector search with graph retrieval and provisionally chose PostgreSQL/pgvector with learned embeddings. [pgvector](https://github.com/pgvector/pgvector#querying) documents exact nearest-neighbor search as its default; [Neo4j](https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/) describes nodes, relationships, and properties. For this small corpus, a graph would add entity resolution and provenance validation without an established multi-hop need.

The build keeps the plan's versioned source set, source-to-citation trace, exact-ranking baseline, and five proposed checks. It uses sparse vectors and SQLite instead of adding PostgreSQL and a model service to the existing 1 GB server. Read-only inspection reported approximately 474 MB available memory before deployment. No provider configuration has been confirmed in this chat. This is an operational choice for a first working **extractive prototype**, not evidence that sparse retrieval outperforms learned embeddings. No vector-versus-graph benchmark was run.

**Unfinished:** learned embeddings, pgvector storage, and model-backed answer generation. This is not a completed generative RAG system. Adding a provider requires server-side configuration, costs/quotas, grounded-generation tests, and a new deployment. No credentials belong in Git or query evidence.

**Known limits:** 15 paragraphs cover only a small part of PostgreSQL 18. Vocabulary expansion is narrow. A topic guard declines questions without COPY/json terms; lexical relevance does not prove that a question is answered. Unsupported questions containing those terms can still return adjacent material. The displayed score is similarity, not confidence. Answers are quotations, not synthesized instructions. Imports share a bounded append-only index; queries filter to the visitor's selected set, but the app is not a private document store. There is no end-user corpus deletion or arbitrary-source import. The Docker volume survives container recreation; no backup/restore drill was run.
