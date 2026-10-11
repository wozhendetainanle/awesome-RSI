# Daily RSI arXiv automation

Generate and publish a daily RSI digest here at 09:00 Beijing time (UTC+8). The user has authorized normal commits and pushes to this repository. Do not modify other research projects or send email or chat messages to others.

All Markdown descriptions must use English, including README, digests, headings, tables, card labels, analysis, research ideas, and source notes. Retain Chinese only in the complete [ZH] abstract bodies. Each paper must keep independent [EN/ZH] disclosure controls.

## Scope and selection

Use the README's three tiers: A, direct RSI; B, self-improvement mechanisms; C, evaluation and limits. Assess relevance through feedback, modification, verification, and subsequent reuse. Cover evolving agents, automated research, training loops, reusable code and harnesses, skill and memory evolution, and environment–supervision co-evolution. Identify whether the changed component is model weights, external code, prompts or skills, memory, or the state of a single inference.

Prioritize the official `https://arxiv.org/list/cs/new?show=2000` and `https://arxiv.org/list/stat.ML/new?show=2000` listings. The CS aggregate includes AI, LG, CL, MA, SE, RO, CV, NE, and CR; add other categories only for a clear topical reason. Search synonymous expressions such as self-improvement, self-evolving, self-modification, harness/skill evolution, recursive improvement, automated research, experience consolidation, and co-evolution, then assess titles and complete abstracts semantically. Keyword matches or title acronyms alone are insufficient.

Include at most 100 papers per digest; publish fewer when appropriate. Include relevant theory and negative results rather than selecting only papers whose authors claim success.

## Retrieval and deduplication

1. Fix the current Beijing date, inspect Git status and the latest run record, and fetch normally. Synchronize by fast-forward when there are no changes to protect. Do not discard, stash, overwrite, or commit unrelated user work.
2. Cache official listings and record each page's actual batch date and complete New/Cross/Replacement section counts. Check `showing X of Y` and paginate if necessary. Save compressed snapshots in `data/sources/YYYY-MM-DD/`, recording relative paths, URLs, and original HTML SHA-256 hashes.
3. Select main-list candidates only from New sections, deduplicate by versionless arXiv ID across sources, and exclude IDs already present in enrichment, digests, or run records. The first run uses the latest official batch. Subsequent runs cover unprocessed batches since the last successful run; after interruptions spanning multiple weekdays, inspect official date archives and recover each missed batch rather than assuming `/new` contains them all.
4. Record collection and announcement dates separately. On weekends, holidays, or unchanged batches, write a short, source-supported digest and update the index and record without repeating papers or cards. Network failures, HTTP 403/429, timeouts, or parsing errors do not mean no new papers exist. Record incomplete coverage and continue checks that remain possible.
5. Limit concurrency and reuse caches. Back off after HTTP 429 rather than retrying densely. A temporary working connection may be used for a network-path failure; do not change permanent proxy settings. Do not present old cached pages as freshly retrieved.
6. Exclude Cross-listings from the main list. List replacements separately only after verifying both version and substantive content changes, and report whether individual replacement checks were performed.

## Evidence and content for each paper

- Obtain titles, authors, categories, and complete English abstracts from official listings, abstract pages, or the original paper. Preserve the original abstract and source URL.
- Each card must contain independent **[EN / ZH] abstract controls**: `[EN] Abstract` displays the complete English original and `[ZH] Abstract` displays the complete Chinese translation, both inside GitHub-supported `<details><summary>` blocks. Users can expand or collapse either language for any paper independently. Neither external links nor summary bullets replace full abstracts.
- Translate the complete abstract faithfully, preserving numbers, abbreviations, task conditions, citation markers, limitations, and claim strength. Do not add full-paper conclusions or editorial analysis. Explicitly flag unresolved macros and metadata conflicts; consult the PDF when HTML is inconsistent rather than guessing missing content.
- Verify affiliations from the paper's first page or a trusted project page and save `affiliation_source`. Display `Affiliation unconfirmed` when verification fails; do not infer institutions from names or email addresses.
- Write 3–5 English analysis bullets per paper covering the update target, feedback and acceptance mechanism, author-reported findings, and evidence limits. Mark ranking and interpretation as inference; do not present unreplicated results as independently verified.
- Add `code`, `project`, `video`, and `data` only after opening and verifying them. Third-party repositories cited by a paper are not its own code. A promise to release after acceptance is not an existing release. Venue claims also require a primary source.
- Use genuine figures from the paper's HTML or PDF and retain `image_source`. For PDF crops, record page, figure/algorithm number, and crop location. Use an explicit placeholder only when a figure cannot be obtained, and report missing-figure counts.

## Outputs and commands

Write `daily/YYYY/YYYY-MM-DD.md` with a title, three-column cards, retrieval overview, tiered Top papers table, per-paper analysis, up to five recommended reads, up to ten research ideas for limited compute budgets, exclusions and source notes as needed, and replacement status. All descriptive prose and labels must be English; only [ZH] abstract bodies are Chinese.

Each research idea must include a concrete method change, an executable minimal experiment and control, budget rationale, expected benefit, and risk. Label ideas as unvalidated proposals. Do not rebrand ordinary reproduction, dataset changes, or tuning as methodological innovation.

Maintain `data/enrichment.json`. Required fields are `title`, `authors`, `categories`, `announced_date`, `abstract_en`, `abstract_zh`, `abstract_source`, `affiliation`, `tier`, and `update_target`. Add supplementary sources, resources, and image fields only with reliable evidence. Use English display metadata and `mechanism_en`, `result_en`, and `boundary_en` for analysis. Existing `_zh` fields may remain as translations, but do not insert them into English Markdown analysis.

For new papers, write the table and enrichment first, then run Python with Pillow/pypdf available:

```bash
python3 scripts/fetch_figures.py --date YYYY-MM-DD
python3 scripts/build_cards.py --date YYYY-MM-DD
```

Dependencies are listed in `requirements.txt`. The Codex workspace Python runtime may be used without changing system Python. Automatic extraction failure does not establish that a paper has no figures; extract vector figures using a PDF renderer when necessary and verify manually. The card builder updates only the specified date and must preserve affiliations and both complete expandable abstracts. Cards display `announced_date`, not the collection date as a substitute.

Keep README entirely English, including the latest digest link, Archive headings, new archive rows, and explanations. Update its latest link and Archive each run. Run records retain batch dates, page counts, deduplicated New IDs, inclusion/exclusion rationale, tier counts, figure and abstract coverage, unconfirmed affiliations, resource-check failures, and validation results. Never save credentials or private personal data. If no new batch exists, update only the short digest, index, and relevant retrieval record.

## Validation and publication

1. Match selected IDs, table rows, cards, and analysis sections without duplicates. **EN abstract count = ZH abstract count = card count = selected paper count.** Check complete paired abstracts and independent disclosure controls.
2. Verify local links and figures exist, decode correctly, and match their papers. Explicitly report placeholders and missing abstracts.
3. Preserve distinctions between facts, author reports, theory, simulation, independent reproduction, and inference. Abstract-level evidence does not establish full-paper review or reproduction.
4. Check README links and dates, batch versus collection dates, deduplication, snapshots, and run records for consistency. Check that Chinese text appears only inside [ZH] abstract bodies across Markdown outputs.
5. Run `git diff --check`. Stage only the current digest, README, required enrichment, figures, and source/run records. Include maintenance rules or tools only when they were intentionally changed.
6. Commit and push normally; never force push. If HTTPS credentials are unavailable, an already authorized SSH remote may be used without exposing credentials. Verify local HEAD against the remote branch SHA and inspect worktree status. Report the actual error and local commit if pushing fails.

The local Codex automation ID is `rsi-arxiv`. This repository has no second GitHub Actions scheduler. The computer and Codex application must be running at execution time. Notify only for a meaningful publication, failure, or required user action; stay quiet when the official batch is unchanged and nothing requires attention.
