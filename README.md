# awesome-RSI

Daily coverage of **Recursive Self-Improvement (RSI)** and related research on arXiv, with curated papers, **[EN / ZH] bilingual abstracts**, original paper figures, mechanism analysis, and research ideas for limited compute budgets.

**Latest digest: [2026-10-15 · 50 papers](daily/2026/2026-10-15.md)**

The first run covers the official **2026-10-09 New submissions** batch. The collection date and announcement batch date are recorded separately.

## Scope

| Tier | Focus | Evidence requirements |
|---|---|---|
| A · Direct RSI | Systems that use their improvements to drive subsequent improvement of models, code, agent harnesses, or research workflows | Identify what changes, its feedback and validation, and how the result is reused; finite rounds do not establish unbounded improvement |
| B · Self-improvement mechanisms | Evolving skills, experience and memory; automated research; self-modifying code; model–supervision or model–environment co-evolution | Require an explicit mechanism for accumulation, modification, or reuse; ordinary agent applications are not automatically included |
| C · Evaluation and limits | Evolving verifiers, reward hacking, stability, theoretical limits, independent transfer, and cost evaluation | Distinguish theory, simulation, author-reported results, and independent replication; include negative findings |

The main list includes official **New submissions**, deduplicated by arXiv ID. Cross-listings are excluded from the main list; verified substantial replacements are listed separately. Keywords aid discovery, while inclusion depends on the title and full abstract. Terms such as `RSI`, `recursive`, `agent`, or `memory` alone do not establish relevance.

## Daily updates

- **Schedule:** Every day at **09:00 Beijing time (UTC+8)** through a local Codex automation. The computer and application must be running when it executes.
- **Content:** A three-column paper card grid, full English and Chinese abstracts, original figures with sources, a tiered paper table, English analysis for each paper, up to five recommended reads, and up to ten research ideas for limited compute budgets. All Markdown descriptions, headings, labels, and documentation use English; Chinese is retained only in the [ZH] abstract bodies.
- **Language controls:** Each card has independent `[EN]` and `[ZH]` disclosure controls. Collapse one abstract and expand the other to switch languages for that paper without affecting other cards.
- **Verification:** Paper metadata links to primary sources. Unconfirmed affiliations are explicitly marked. Code, project, video, and dataset links are added only after verification. Research ideas are labeled as unvalidated proposals.
- **Unchanged batches:** Record the official batch date and reason without repeating previously covered papers. Retrieval failures are reported as failures, not as evidence that no new papers exist.

## Archive

| Collection date (Beijing) | Official batch | Papers | A / B / C | Digest |
|---|---|---:|---|---|
| 2026-10-15 | 2026-10-14 | 50 | 23 / 13 / 14 | [Read](daily/2026/2026-10-15.md) |
| 2026-10-14 | 2026-10-12 (unchanged) | 0 | 0 / 0 / 0 | [Read](daily/2026/2026-10-14.md) |
| 2026-10-13 | 2026-10-12 | 41 | 6 / 25 / 10 | [Read](daily/2026/2026-10-13.md) |
| 2026-10-12 | 2026-10-09 (unchanged) | 0 | 0 / 0 / 0 | [Read](daily/2026/2026-10-12.md) |
| 2026-10-11 | 2026-10-09 | 35 | 12 / 14 / 9 | [Read](daily/2026/2026-10-11.md) |

## Repository structure

- `daily/YYYY/YYYY-MM-DD.md`: Daily digests, readable directly on GitHub.
- `data/enrichment.json`: Original abstracts, translations, affiliations, verified resources, and image sources, keyed by arXiv ID.
- `data/runs/YYYY-MM-DD.json`: Announcement batches, counts, deduplicated and selected IDs, and verification records.
- `data/sources/YYYY-MM-DD/`: Compressed snapshots of official listings for source auditing.
- `assets/papers/YYYY-MM-DD/`: Original paper illustrations.
- `scripts/`: Figure extraction and per-digest card generation tools.

See [AUTOMATION.md](AUTOMATION.md) for the full workflow. Helper scripts are adapted from the same maintainer's [Daily-Arxiv](https://github.com/wozhendetainanle/Daily-Arxiv/tree/0461680a83c2be9c3a87c41a8661bea4e9ee969f/scripts). Card generation updates only the specified date to preserve historical digests.
