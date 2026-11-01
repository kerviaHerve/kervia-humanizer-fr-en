# Local preservation checker

Python 3.10+; standard library only. The script reads two UTF-8 files, emits JSON and changes neither file. It makes no model or network call.

Run through the agent's terminal tool, using actual installed paths:

```text
python3 scripts/check_preservation.py original.md revision.md
python3 scripts/check_preservation.py original.md revision.md --manifest pins.json
```

An optional manifest contains exact strings already present in the source:

```json
{"exact": ["dossier complet", "sauf disposition légale contraire"]}
```

It checks inventories of common quotations, code, frontmatter, URLs, numbers and explicit pins. Duplicates count. Reports contain fragment hashes rather than the fragments themselves.

| Exit | Meaning |
|---|---|
| 0 | No mechanical issue detected; semantic review is still required. |
| 2 | Review the reported changes. A permitted reformat can also trigger an alert. |
| 3 | Invalid invocation, unreadable/oversized input or invalid manifest. No successful check. |

The result always keeps `meaning_verified: false`. The same numbers can describe different quantities after a swap. Units, modality, negation, attribution and scope are not semantically validated. A pin verifies literal occurrence and count, not its meaning or location.

This is not a full Markdown/HTML parser. Unusual URLs or syntax need an explicit pin or manual review. Inputs are limited to 2 MiB each. Do not claim that checking an excerpt checks the complete document.

The script itself uses no LLM tokens. An agent may still spend tokens reading instructions, invoking a tool and reading its JSON result. The prompt benchmark measures its documented editing path, not an entire tool-using agent session.
