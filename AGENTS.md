# Project rules

This repository contains a public bilingual writing skill, its local checker and reproducible experiments.

- Keep one runtime `SKILL.md` at the root. Vendored benchmark baselines are labelled data, not additional installable skills.
- Publish no secrets, private configurations, user conversations, unpublished client text or machine-specific paths.
- Main instructions and one language module form the normal editing path. Benchmarks and examples are not runtime context.
- Preserve attributed inspirations and third-party licences. Do not present a baseline as our own implementation.
- Run `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` before publication.
- Record actual benchmark prompts, final outputs, model label, requested settings, usage and failures. Missing usage is unavailable, never guessed from words.
- Benchmark the same text and common task instruction in fresh request contexts. Do not tune after looking at a preferred outcome or claim a tiny pilot proves universal superiority.
- Keep factual fidelity, user preference, detector classifications and token usage separate. A mechanical pass does not verify meaning.
- Do not start another agent, publish private source history or change account permissions for this work.
