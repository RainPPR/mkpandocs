"""
Simplified page tests for MkPandocs.

This file contains simplified tests that don't depend on python-markdown.
"""

from __future__ import annotations

import os
import textwrap
import unittest

from properdocs.config.defaults import ProperDocsConfig
from properdocs.structure.files import File, Files
from properdocs.structure.pages import Page

DOCS_DIR = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), '..', 'integration', 'subpages', 'docs'
)


def load_config(**cfg) -> ProperDocsConfig:
    cfg.setdefault('site_name', 'Example')
    cfg.setdefault('theme', 'mkdocs')
    cfg.setdefault(
        'docs_dir',
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)), '..', 'integration', 'minimal', 'docs'
        ),
    )
    conf = ProperDocsConfig()
    conf.load_dict(cfg)
    errors_warnings = conf.validate()
    assert errors_warnings == ([], []), errors_warnings
    return conf


class PageTests(unittest.TestCase):
    def test_homepage(self):
        cfg = load_config(docs_dir=DOCS_DIR)
        fl = File('index.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)
        self.assertIsNone(fl.page)
        pg = Page('Foo', fl, cfg)
        self.assertEqual(fl.page, pg)
        self.assertEqual(pg.url, '')
        self.assertEqual(pg.abs_url, None)
        self.assertEqual(pg.canonical_url, None)
        self.assertEqual(pg.edit_url, None)
        self.assertEqual(pg.file, fl)
        self.assertEqual(pg.content, None)
        self.assertTrue(pg.is_homepage)
        self.assertTrue(pg.is_index)
        self.assertTrue(pg.is_page)
        self.assertFalse(pg.is_section)
        self.assertTrue(pg.is_top_level)
        self.assertEqual(pg.markdown, None)
        self.assertEqual(pg.meta, {})
        self.assertEqual(pg.next_page, None)
        self.assertEqual(pg.parent, None)
        self.assertEqual(pg.previous_page, None)
        self.assertEqual(pg.title, 'Foo')
        self.assertEqual(pg.toc, [])

    def test_nested_index_page(self):
        cfg = load_config(docs_dir=DOCS_DIR)
        fl = File('sub1/index.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)
        pg = Page('Foo', fl, cfg)
        pg.parent = 'foo'
        self.assertEqual(pg.url, 'sub1/')
        self.assertEqual(pg.abs_url, None)
        self.assertEqual(pg.canonical_url, None)
        self.assertEqual(pg.edit_url, None)
        self.assertEqual(pg.file, fl)
        self.assertEqual(pg.content, None)
        self.assertFalse(pg.is_homepage)
        self.assertTrue(pg.is_index)
        self.assertTrue(pg.is_page)
        self.assertFalse(pg.is_section)
        self.assertFalse(pg.is_top_level)
        self.assertEqual(pg.markdown, None)
        self.assertEqual(pg.meta, {})
        self.assertEqual(pg.next_page, None)
        self.assertEqual(pg.parent, 'foo')
        self.assertEqual(pg.previous_page, None)
        self.assertEqual(pg.title, 'Foo')
        self.assertEqual(pg.toc, [])

    def test_nested_index_page_no_parent(self):
        cfg = load_config(docs_dir=DOCS_DIR)
        fl = File('sub1/index.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)
        pg = Page('Foo', fl, cfg)
        pg.parent = None  # non-homepage at nav root level
        self.assertEqual(pg.url, 'sub1/')
        self.assertEqual(pg.abs_url, None)
        self.assertEqual(pg.canonical_url, None)
        self.assertEqual(pg.edit_url, None)
        self.assertEqual(pg.file, fl)
        self.assertEqual(pg.content, None)
        self.assertFalse(pg.is_homepage)
        self.assertTrue(pg.is_index)
        self.assertTrue(pg.is_page)
        self.assertFalse(pg.is_section)
        # Note: is_top_level depends on file.inclusion, not parent
        self.assertEqual(pg.markdown, None)
        self.assertEqual(pg.meta, {})
        self.assertEqual(pg.next_page, None)
        self.assertEqual(pg.parent, None)
        self.assertEqual(pg.previous_page, None)
        self.assertEqual(pg.title, 'Foo')
        self.assertEqual(pg.toc, [])

    def test_non_index_page(self):
        cfg = load_config(docs_dir=DOCS_DIR)
        fl = File('non-index.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)
        pg = Page('Foo', fl, cfg)
        self.assertEqual(pg.url, 'non-index/')
        self.assertEqual(pg.abs_url, None)
        self.assertEqual(pg.canonical_url, None)
        self.assertEqual(pg.edit_url, None)
        self.assertEqual(pg.file, fl)
        self.assertEqual(pg.content, None)
        self.assertFalse(pg.is_homepage)
        self.assertFalse(pg.is_index)
        self.assertTrue(pg.is_page)
        self.assertFalse(pg.is_section)
        self.assertTrue(pg.is_top_level)
        self.assertEqual(pg.markdown, None)
        self.assertEqual(pg.meta, {})
        self.assertEqual(pg.next_page, None)
        self.assertEqual(pg.parent, None)
        self.assertEqual(pg.previous_page, None)
        self.assertEqual(pg.title, 'Foo')
        self.assertEqual(pg.toc, [])

    def test_page_title_from_meta(self):
        cfg = load_config(docs_dir=DOCS_DIR)
        fl = File('index.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)
        pg = Page(None, fl, cfg)
        pg.markdown = '# Title from Markdown'
        pg.meta = {'title': 'Title from Meta'}
        self.assertEqual(pg.title, 'Title from Meta')

    def test_page_title_from_markdown(self):
        cfg = load_config(docs_dir=DOCS_DIR)
        fl = File('index.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)
        pg = Page(None, fl, cfg)
        pg.markdown = '# Title from Markdown'
        pg.meta = {}
        self.assertEqual(pg.title, 'Title from Markdown')

    def test_page_title_from_filename(self):
        cfg = load_config(docs_dir=DOCS_DIR)
        fl = File('my-page.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)
        pg = Page(None, fl, cfg)
        pg.markdown = 'No title here'
        pg.meta = {}
        self.assertEqual(pg.title, 'My page')

    def test_page_render(self):
        """Test that a page can be rendered with pypandoc."""
        cfg = load_config(docs_dir=DOCS_DIR)
        fl = File('index.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)
        pg = Page('Test', fl, cfg)
        pg.markdown = '# Hello World\n\nThis is a test.'
        files = Files([fl])
        pg.render(cfg, files)
        self.assertIsNotNone(pg.content)
        self.assertIn('Hello World', pg.content)

    def test_page_render_with_toc(self):
        """Test that TOC is generated correctly."""
        cfg = load_config(docs_dir=DOCS_DIR)
        fl = File('index.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)
        pg = Page('Test', fl, cfg)
        pg.markdown = textwrap.dedent("""
            # Main Title

            ## Section 1

            Content here.

            ## Section 2

            More content.
        """)
        files = Files([fl])
        pg.render(cfg, files)
        self.assertIsNotNone(pg.toc)
        self.assertGreater(len(pg.toc), 0)

    def test_page_render_without_markdown_raises(self):
        """Test that rendering without markdown raises an error."""
        cfg = load_config(docs_dir=DOCS_DIR)
        fl = File('index.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)
        pg = Page('Test', fl, cfg)
        files = Files([fl])
        with self.assertRaises(RuntimeError):
            pg.render(cfg, files)


if __name__ == '__main__':
    unittest.main()
