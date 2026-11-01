from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('paired_benchmark', ROOT / 'benchmarks/run_compare.py')
assert spec and spec.loader
bench = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bench)


class BenchmarkContractTests(unittest.TestCase):
    def test_required_literals_exist_in_fictional_inputs(self):
        data = json.loads((ROOT / 'benchmarks/cases.json').read_text(encoding='utf-8'))
        self.assertIn('fictional', data['kind'])
        self.assertEqual(len({c['id'] for c in data['cases']}), len(data['cases']))
        for case in data['cases']:
            prompt, source = bench.task(case)
            self.assertTrue(all(pin in source for pin in case['required_strings']))
            self.assertIn(source, prompt)
            self.assertIn('final text only', prompt)

    def test_reference_is_full_and_pinned(self):
        reference = ROOT / 'benchmarks/baselines/humanizer-3.1.0.md'
        meta = json.loads((reference.parent / 'source.json').read_text())
        self.assertEqual(hashlib.sha256(reference.read_bytes()).hexdigest(), meta['sha256'])
        self.assertEqual(bench.instruction('humanizer', 'fr')[0], reference.read_text())
        self.assertEqual(meta['version'], '3.1.0')

    def test_only_one_language_module_is_loaded(self):
        text, files = bench.instruction('kervia', 'fr')
        self.assertEqual(set(files), {'SKILL.md', 'references/fr.md'})
        self.assertIn((ROOT / 'references/fr.md').read_text(), text)
        self.assertNotIn((ROOT / 'references/en.md').read_text(), text)
        self.assertNotIn((ROOT / 'references/deep-edit.md').read_text(), text)

    def test_invalid_arm_or_language_is_rejected(self):
        for arm, language in [('unknown', 'fr'), ('kervia', 'xx')]:
            with self.subTest(arm=arm, language=language), self.assertRaises(ValueError):
                bench.instruction(arm, language)

    def test_common_output_contract_overrides_default_audits(self):
        self.assertIn('overrides default output-format', bench.COMMON_SYSTEM)
        self.assertIn('no draft, audit', bench.COMMON_SYSTEM)

    def test_case_path_cannot_escape(self):
        for file in ['../../outside.txt', '/absolute.txt']:
            with self.subTest(file=file), self.assertRaises(ValueError):
                bench.case_path({'file': file})

    def test_local_endpoint_default(self):
        self.assertEqual(bench.endpoint('http://127.0.0.1:8080/v1', False), 'http://127.0.0.1:8080/v1/chat/completions')

    def test_remote_requires_explicit_permission(self):
        with self.assertRaises(ValueError):
            bench.endpoint('https://example.invalid/v1', False)
        self.assertEqual(bench.endpoint('https://example.invalid/v1', True), 'https://example.invalid/v1/chat/completions')

    def test_secret_in_url_is_rejected(self):
        with self.assertRaises(ValueError):
            bench.endpoint('https://user:example@example.invalid/v1', True)

    def test_queries_and_fragments_are_rejected(self):
        for suffix in ['?key=example', '#fragment']:
            with self.subTest(suffix=suffix), self.assertRaises(ValueError):
                bench.endpoint('http://localhost:8080/v1' + suffix, False)

    def test_mocked_usage_is_checked_not_estimated(self):
        # These unit-test values are not benchmark observations.
        usage = {'prompt_tokens': 10, 'completion_tokens': 5, 'total_tokens': 15}
        self.assertEqual(bench.checked_usage({'usage': usage}), usage)

    def test_missing_usage_is_unavailable(self):
        for response in [{}, {'usage': {}}, {'usage': {'prompt_tokens': '10'}}]:
            with self.subTest(response=response), self.assertRaises(ValueError):
                bench.checked_usage(response)

    def test_inconsistent_usage_is_rejected(self):
        with self.assertRaises(ValueError):
            bench.checked_usage({'usage': {'prompt_tokens': 10, 'completion_tokens': 5, 'total_tokens': 14}})

    def test_mocked_partial_pairs_have_no_reduction_claim(self):
        data = {'cases': [{'id': 'mock'}], 'records': []}
        result = bench.summary(data)
        self.assertFalse(result['all_pairs_completed'])
        self.assertIsNone(result['reduction_percent'])

    def test_mocked_totals_are_programmatically_computed(self):
        data = {'cases': [{'id': 'mock'}], 'records': [
            {'case': 'mock', 'arm': 'humanizer', 'status': 'completed', 'usage': {'prompt_tokens': 100, 'completion_tokens': 20, 'total_tokens': 120}},
            {'case': 'mock', 'arm': 'kervia', 'status': 'completed', 'usage': {'prompt_tokens': 60, 'completion_tokens': 20, 'total_tokens': 80}}]}
        result = bench.summary(data)
        self.assertEqual(result['reduction_percent']['total_tokens'], 100 * (120 - 80) / 120)
        self.assertFalse(result['quality_or_authorship_verified'])

    def test_public_runtime_has_one_skill_and_standard_metadata(self):
        skills = list(ROOT.rglob('SKILL.md'))
        self.assertEqual(skills, [ROOT / 'SKILL.md'])
        text = skills[0].read_text()
        self.assertIn('name: kervia-humanizer-fr-en', text)
        self.assertIn('license: MIT', text)
        self.assertIn('version: "0.1.0"', text)
        for name in ['SKILL.md', 'references/fr.md', 'references/en.md', 'references/deep-edit.md']:
            content = (ROOT / name).read_text()
            self.assertNotIn('/home/', content)
            self.assertNotIn('/STORAGE', content)

    def test_attribution_and_licences_are_present(self):
        self.assertIn('Inspired by', (ROOT / 'THIRD_PARTY_NOTICES.md').read_text())
        self.assertIn('blader/humanizer', (ROOT / 'THIRD_PARTY_NOTICES.md').read_text())
        self.assertIn('Copyright (c) 2025 Siqi Chen', (ROOT / 'benchmarks/baselines/HUMANIZER-LICENSE.txt').read_text())
        self.assertIn('Copyright (c) 2026 Hervé Barrilliet', (ROOT / 'LICENSE').read_text())

    def test_published_observations_match_their_current_prompts(self):
        for path in (ROOT / 'benchmarks/results').glob('*.json'):
            data = json.loads(path.read_text())
            self.assertTrue(data['summary']['all_pairs_completed'], path.name)
            self.assertEqual(data['summary'], bench.summary(data))
            cases = {c['id']: c for c in data['cases']}
            for record in data['records']:
                case = cases[record['case']]
                skill, hashes = bench.instruction(record['arm'], record['language'])
                user, source = bench.task(case)
                self.assertEqual(record['instruction_files'], hashes)
                self.assertEqual(record['system_sha256'], bench.sha(bench.COMMON_SYSTEM + skill + '\n</skill>'))
                self.assertEqual(record['task_sha256'], bench.sha(user))
                self.assertEqual(record['source_sha256'], bench.sha(source))
                self.assertEqual(record['usage'], bench.checked_usage({'usage': record['usage']}))
                self.assertFalse(record['mechanical']['meaning_verified'])


if __name__ == '__main__':
    unittest.main()
