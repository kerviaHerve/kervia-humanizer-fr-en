#!/usr/bin/env python3
"""Offline mechanical preservation checks, not semantic or authorship detection.

Exit 0: no mechanical issue detected; 2: review required; 3: invalid input.
Never rewrites input files, executes their contents or calls a network service.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import NoReturn

MAX_BYTES = 2 * 1024 * 1024
NUMBER = re.compile(r"(?<![\w])[-+\u2212]?\d+(?:(?:[.,]\d+)|(?:[ \u00a0\u202f]\d{3}(?!\d)))*(?!\d)")
URL = re.compile(r'''https?://[^\s<>\[\]"']+''')
QUOTE = re.compile(r'«[^»]*»|“[^”]*”|(?<!\w)"[^"\n]+"(?!\w)', re.DOTALL)
INLINE_CODE = re.compile(r'(?<!`)(`+)(?!`)(.+?)(?<!`)\1(?!`)', re.DOTALL)
FRONTMATTER = re.compile(r'\A(?:\ufeff)?---[ \t]*\r?\n.*?\r?\n---[ \t]*(?:\r?\n|\Z)', re.DOTALL)


def digest(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def read_text(path: Path) -> str:
    # Read at most the documented bound, including files whose size changes.
    with path.open('rb') as handle:
        data = handle.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError('Input exceeds the 2 MiB limit.')
    return data.decode('utf-8')


def mask(text: str, spans: list[tuple[int, int]]) -> str:
    chars = list(text)
    for start, end in spans:
        chars[start:end] = ' ' * (end - start)
    return ''.join(chars)


def protected(text: str) -> tuple[Counter, list[tuple[int, int]]]:
    """Extract conservative literal islands, preserving duplicates.

    Common Markdown only, not a complete Markdown/HTML parser. Frontmatter
    and fenced blocks are extracted before inline code, quotes and URLs.
    """
    items: Counter = Counter()
    spans: list[tuple[int, int]] = []
    fm = FRONTMATTER.match(text)
    if fm:
        items[('frontmatter', fm.group())] += 1
        spans.append(fm.span())

    # Fences allow up to three leading spaces and a closing fence at least
    # as long as its opener. An unclosed fence protects through end of input.
    lines = text.splitlines(keepends=True)
    offset = 0
    opened = None
    for line in lines:
        if not any(start <= offset < end for start, end in spans):
            opening = re.match(r' {0,3}(`{3,}|~{3,})([^\r\n]*)', line)
            if opened is None and opening:
                token = opening.group(1)
                # Backticks inside a backtick info string do not open a fence.
                if token[0] != '`' or '`' not in opening.group(2):
                    opened = (offset, token[0], len(token))
            elif opened is not None:
                close = re.fullmatch(r' {0,3}' + re.escape(opened[1]) +
                                     '{' + str(opened[2]) + r',}[ \t]*(?:\r?\n)?', line)
                if close:
                    end = offset + len(line)
                    items[('fenced_code', text[opened[0]:end])] += 1
                    spans.append((opened[0], end))
                    opened = None
        offset += len(line)
    if opened:
        items[('fenced_code', text[opened[0]:])] += 1
        spans.append((opened[0], len(text)))

    for kind, expression in [('inline_code', INLINE_CODE), ('quotation', QUOTE), ('url', URL)]:
        visible = mask(text, spans)
        for match in expression.finditer(visible):
            start, end = match.span()
            if kind == 'url':
                # Terminal prose punctuation is ambiguous. Explicit manifest
                # pins handle URLs ending in such characters or nested markup.
                trimmed = match.group().rstrip('.,;!?')
                # Keep balanced parentheses in a URL, but drop Markdown closers.
                while trimmed.endswith(')') and trimmed.count(')') > trimmed.count('('):
                    trimmed = trimmed[:-1]
                end = start + len(trimmed)
            if end > start:
                literal = text[start:end]
                items[(kind, literal)] += 1
                spans.append((start, end))
    return items, spans


def validate_manifest(data: object, source: str) -> list[str]:
    if not isinstance(data, dict) or set(data) - {'exact'}:
        raise ValueError('Manifest must be an object with only an exact array.')
    pins = data.get('exact', [])
    if not isinstance(pins, list) or any(not isinstance(x, str) or not x for x in pins):
        raise ValueError('Manifest exact must contain non-empty strings.')
    pins = list(dict.fromkeys(pins))
    if any(pin not in source for pin in pins):
        raise ValueError('A manifest pin does not occur in the source.')
    return pins


def compare(source: str, output: str, manifest: object | None = None) -> dict:
    source_items, source_spans = protected(source)
    output_items, output_spans = protected(output)
    pins = validate_manifest(manifest if manifest is not None else {}, source)
    issues = []
    for kind, literal in sorted(set(source_items) | set(output_items)):
        before = source_items[(kind, literal)]
        after = output_items[(kind, literal)]
        if before != after:
            issues.append({'kind': kind, 'fragment_sha256': digest(literal),
                           'source_count': before, 'output_count': after,
                           'reason': 'protected_literal_inventory_changed'})
    for pin in pins:
        before, after = source.count(pin), output.count(pin)
        if before != after:
            issues.append({'kind': 'manifest_pin', 'fragment_sha256': digest(pin),
                           'source_count': before, 'output_count': after,
                           'reason': 'explicit_literal_count_changed'})

    source_numbers = Counter(NUMBER.findall(mask(source, source_spans)))
    output_numbers = Counter(NUMBER.findall(mask(output, output_spans)))
    for number in sorted(set(source_numbers) | set(output_numbers)):
        before, after = source_numbers[number], output_numbers[number]
        if before != after:
            issues.append({'kind': 'number', 'fragment_sha256': digest(number),
                           'source_count': before, 'output_count': after,
                           'reason': 'numeric_inventory_changed_not_semantically_verified'})
    if '\u2014' in mask(output, output_spans):
        issues.append({'kind': 'house_style', 'reason': 'em_dash_in_unprotected_prose'})
    return {
        'schema_version': 1,
        'status': 'review_required' if issues else 'no_mechanical_issue_detected',
        'semantic_review_required': True,
        'meaning_verified': False,
        'authorship_assessed': False,
        'source_sha256': digest(source),
        'output_sha256': digest(output),
        'issue_count': len(issues),
        'issues': issues,
        'limits': [
            'Does not validate facts, attribution, units, negation, scope or commitments.',
            'Same literal inventory can accompany a different meaning.',
            'Does not parse all Markdown, HTML, citations or mathematical notation.',
            'Reformatting numbers can trigger review even when values are equivalent.',
            'A manifest pin checks literal presence and count, not location or meaning.',
        ],
    }


class InputParser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        # Keep malformed invocations distinct from a real review result.
        raise ValueError('Invalid command line.')


def main(argv: list[str] | None = None) -> int:
    parser = InputParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--manifest', type=Path, help='Optional JSON with an exact string array.')
    try:
        args = parser.parse_args(argv)
        original, revised = read_text(args.source), read_text(args.output)
        manifest = json.loads(read_text(args.manifest)) if args.manifest else None
        result = compare(original, revised, manifest)
    except (OSError, UnicodeError, ValueError) as exc:
        # Do not echo source text, manifest literals or a JSON decoding excerpt.
        error_kind = type(exc).__name__
        print(json.dumps({'status': 'invalid_input', 'error_kind': error_kind,
                          'meaning_verified': False}, ensure_ascii=False))
        return 3
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if result['issues'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
