import re
import subprocess
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / 'templates' / 'index.html'


class IdCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.data_scroll_targets = []

    def handle_starttag(self, tag, attrs):
        attr_map = dict(attrs)
        if 'id' in attr_map:
            self.ids.add(attr_map['id'])
        if 'data-scroll' in attr_map:
            self.data_scroll_targets.append(attr_map['data-scroll'])


class FrontendTemplateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = TEMPLATE.read_text(encoding='utf-8')
        script_match = re.search(r'<script>\n(.*)\n</script>', cls.html, flags=re.S)
        if not script_match:
            raise AssertionError('Expected inline <script> block was not found in templates/index.html')
        cls.script = script_match.group(1)

    def test_inline_javascript_syntax_is_valid(self):
        with tempfile.NamedTemporaryFile('w', suffix='.js', encoding='utf-8', delete=False) as temp_js:
            temp_js.write(self.script)
            temp_path = temp_js.name

        result = subprocess.run(['node', '--check', temp_path], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)

    def test_referenced_ids_exist(self):
        parser = IdCollector()
        parser.feed(self.html)
        referenced_ids = set(re.findall(r"\$\('([^']+)'\)", self.script))
        missing = sorted(referenced_ids - parser.ids)
        self.assertEqual(missing, [], msg=f'Missing DOM ids in template: {missing}')

    def test_data_scroll_targets_exist(self):
        parser = IdCollector()
        parser.feed(self.html)
        missing_targets = sorted(set(parser.data_scroll_targets) - parser.ids)
        self.assertEqual(missing_targets, [], msg=f'Missing scroll target ids: {missing_targets}')


if __name__ == '__main__':
    unittest.main()
