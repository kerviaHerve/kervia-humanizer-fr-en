"""Native Hermes loader check; run only in a marked disposable home."""
import json
import os
from pathlib import Path
import unittest

NAME = 'kervia-humanizer-fr-en'

class NativeLoaderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        home = Path(os.environ.get('HERMES_HOME', '')).resolve()
        if not (home / '.kervia-skill-runtime-test').is_file():
            raise RuntimeError('Disposable marked home required; no user profile will be used.')
        from tools.skills_tool import skill_view
        from tools.skill_manager_tool import _validate_frontmatter
        cls.view = staticmethod(skill_view)
        cls.validate = staticmethod(_validate_frontmatter)

    def test_main_loads_and_validates(self):
        result = json.loads(self.view(NAME))
        self.assertTrue(result.get('success'), result)
        self.assertEqual(result['readiness_status'], 'available')
        self.assertIsNone(self.validate(result['content'], new_skill=True))
        self.assertEqual(result['metadata']['version'], '0.1.1')

    def test_both_language_modules_load(self):
        for path in ['references/fr.md', 'references/en.md', 'references/deep-edit.md']:
            with self.subTest(path=path):
                self.assertTrue(json.loads(self.view(NAME, file_path=path)).get('success'))

    def test_runtime_is_text_only(self):
        result = json.loads(self.view(NAME))
        self.assertTrue(result.get('success'), result)
        linked = result.get('linked_files') or {}
        self.assertFalse(linked.get('scripts'))
        self.assertFalse(linked.get('assets'))
        self.assertTrue((Path(result['skill_dir']) / 'LICENSE').is_file())

if __name__ == '__main__':
    unittest.main()
