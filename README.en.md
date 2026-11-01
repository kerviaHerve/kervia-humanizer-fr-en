# Kervia Humanizer FR/EN

**Experimental version: human review is needed before publication.** The benchmark also exposes style and scope limitations.

Edit French and English prose while preserving facts, qualifications and authorial voice. Draft from supplied notes without fabricating real-world detail. This is an editorial skill, not a detector-evasion tool.

**Inspired by [blader/humanizer](https://github.com/blader/humanizer), by Siqi Chen.** Kervia's runtime rules and local checker were written for this project. An unchanged upstream copy is included only as a labelled benchmark baseline, with its MIT licence. See [attribution](THIRD_PARTY_NOTICES.md).

[Documentation française](README.md)

## Runtime footprint

Load `SKILL.md` and one language module. Read deeper references only when the task needs them; do not load examples, research or benchmarks for an ordinary edit. Return the final text without a mandatory draft or audit. Already good text may remain unchanged.

French has its own scope, modality, terminology and regional guidance. English has its own register and locale guidance. Neither module treats a word or grammatical form as proof of AI authorship.

Preserve every material assertion and exact protected content. A supplied claim is not independently verified. Summarising, translating, inventing fiction and publishing need their own mandate.

## Use

Install only `skills/kervia-humanizer-fr-en/`, the text-only package containing `SKILL.md` and its references. Project code and benchmark data are not installed dependencies. With the Hermes CLI:

```text
hermes skills install kerviaHerve/kervia-humanizer-fr-en/skills/kervia-humanizer-fr-en
```

 In Hermes, load `kervia-humanizer-fr-en` and provide the task. The benchmark baseline is not another runtime skill.

Example: “Lightly edit this British English email. Preserve the names, conditions and commitments. Leave clear passages unchanged.”

## Evidence, not a promise

The [paired benchmark](benchmarks/README.md) uses the same source, model, common task and final-only output contract in separate request contexts. Actual provider usage is saved with raw final outputs.

- [Measured results and limits](benchmarks/results/qwen36-text-runtime-2026-11-01.md)
- [Raw observations](benchmarks/results/qwen36-text-runtime-2026-11-01.json)
- [French example](examples/fr-slop.md), [English example](examples/en-slop.md), [clean-text control](examples/fr-clean.md)

This is a small synthetic development pilot, not an independent preference study or proof of universal superiority. Model load/cache effects make raw timings unsuitable for a speed claim. Failures are retained. No detector score is used as a quality measure.

## Tokens observed in this pilot

| Path | Input | Output | Total |
|---|---:|---:|---:|
| Full Humanizer 3.1.0 | 23501 | 565 | 24066 |
| Kervia core + relevant language | 5099 | 614 | 5713 |

Observed reduction: **78.30% of input tokens** and **76.26% overall** across the three completed pairs. Input counts include provider-reported cached tokens, not measured monetary savings. Kervia outputs are not shorter in aggregate tokens; the reduction is in instruction context.

The [output review](benchmarks/QUALITY.md) also records limits: both methods preserve the clean text, Humanizer gives the English example more informative headings, and one French Kervia formulation needs a scope check. Literal-inventory alerts remain in the raw observations.

## Optional offline checker

This developer tool stays outside the installable package. Using it is an explicit choice; loading the text skill neither downloads nor runs it. See the [installation boundary](SECURITY.md).

```text
python3 scripts/check_preservation.py original.md revision.md
```

The [checker](references/checker.md) makes no model call and changes no input. The agent may spend tokens reading its instructions or result. A mechanical pass never certifies meaning.

## Tests and licence

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

Python 3.10+, standard library only. Tests do not call a model. Native Hermes loader probes require disposable marked homes.

[Validation and its scope](VALIDATION.md).

[MIT](LICENSE). [Research sources and limits](references/sources.md). No model weights, credentials, private conversations or customer material are distributed.
