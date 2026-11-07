"""Exercise rejection paths without modifying the real content or manifest."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

class TranslationGuardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ('en', 'zh', 'scripts'):
            shutil.copytree(ROOT / name, self.root / name, ignore=shutil.ignore_patterns('.quarto'))
        shutil.copy(ROOT / 'translations.json', self.root)

    def run_guard(self, *args):
        return subprocess.run(['python3', str(self.root / 'scripts/check-translations.py'), *args], capture_output=True, text=True)

    def edit(self, lang, name='about.qmd', text='\nUpdated content.\n'):
        p = self.root / lang / name
        p.write_text(p.read_text() + text)

    def test_reviewed_pairs_pass(self):
        self.assertEqual(self.run_guard().returncode, 0)

    def test_missing_translation_fails(self):
        (self.root / 'zh/about.qmd').unlink()
        self.assertNotEqual(self.run_guard().returncode, 0)

    def test_one_sided_change_cannot_be_recorded(self):
        self.edit('en')
        self.assertNotEqual(self.run_guard().returncode, 0)
        self.assertNotEqual(self.run_guard('--record').returncode, 0)

    def test_both_editions_require_review_record(self):
        for lang in ('en', 'zh'):
            self.edit(lang)
        self.assertNotEqual(self.run_guard().returncode, 0)
        self.assertEqual(self.run_guard('--record').returncode, 0)
        self.assertEqual(self.run_guard().returncode, 0)

    def test_formula_drift_fails_even_when_both_edited(self):
        self.edit('en', 'technical-notes/convex-optimization/index.qmd', '\n$$x=9$$\n')
        self.edit('zh', 'technical-notes/convex-optimization/index.qmd', '\n$$x=8$$\n')
        result = self.run_guard('--record')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('display equations', result.stderr)

if __name__ == '__main__':
    unittest.main()
