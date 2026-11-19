# Real hosted browser checks — November 19, 2026

Observer: Codex using the in-app browser. These are AI observations, not student testimony.

| Action/check | Observed result |
| --- | --- |
| Open hosted portfolio | Intro, career direction, project sections, and unfinished labels displayed |
| Click Work | URL reached `/portfolio#work`; DOM measurement showed the work section in the viewport |
| Click Direction | URL reached `/portfolio#direction` |
| Click research-shaped release section | Opened `/portfolio/delivery#release-evidence`; release artifacts and attribution limits displayed |
| Click Docs assistant | Opened `/rag`; three permitted source checkboxes and import control displayed |
| Import all three | UI displayed “15 selected chunks ready; 0 newly inserted. Existing IDs are reused.” (an earlier live API check had already imported the corpus) |
| Ask laptop CSV/remote database question | Displayed client-side and server-side passages, both source links, and a real trace |
| Click displayed psql citation | Opened original `psql` page at `#APP-PSQL-META-COMMANDS-COPY`; supporting client-side entry was present |
| Ask database password question | UI displayed insufficient evidence; no source links in the answer |
| Inspect portfolio at 390px and 1280px widths | DOM measurements reported no horizontal overflow at either width; screenshots saved |
| Open RAG case from project card | Reached `/portfolio/rag`; scope, research, contribution and incomplete generation disclosed |
| Inspect RAG at 1280px and 390px | Screenshots saved and visually inspected; narrow view used a stacked source/question layout. No automated mobile overflow result is claimed here. |

Evidence: [displayed question/answer/source trace](browser-query-trace.json), [unsupported trace](browser-unsupported-trace.json), [portfolio desktop](portfolio-desktop.jpg), [portfolio mobile](portfolio-mobile.jpg), [RAG desktop](rag-desktop.jpg), [RAG mobile](rag-mobile.jpg).

Two browser operations timed out during later navigation. A fresh tab recovered portfolio verification after the first timeout. The second timeout interrupted a final assistant-link revisit and viewport reset; that attempted revisit is not counted as a pass. The earlier assistant link, import, answer, citation and refusal checks above completed successfully. The screenshot files and HTTP checks are independent of the interrupted revisit.

This does not establish accessibility conformance, exhaustive browser compatibility, answer quality outside the recorded questions, or the learner's own observations.
