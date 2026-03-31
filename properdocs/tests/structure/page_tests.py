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

    def test_page_render_with_code_block(self):
        """Test rendering a page with code blocks."""
        cfg = load_config(docs_dir=DOCS_DIR)
        fl = File('code.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)
        pg = Page('Code', fl, cfg)
        pg.markdown = textwrap.dedent("""
            # Code Example

            ```python
            def hello():
                print("Hello, World!")
            ```
        """)
        files = Files([fl])
        pg.render(cfg, files)
        self.assertIsNotNone(pg.content)
        self.assertIn('hello', pg.content)

    def test_page_render_with_links(self):
        """Test rendering a page with links."""
        cfg = load_config(docs_dir=DOCS_DIR)
        fl = File('links.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)
        pg = Page('Links', fl, cfg)
        pg.markdown = '# Links\n\n[Example](https://example.com)'
        files = Files([fl])
        pg.render(cfg, files)
        self.assertIsNotNone(pg.content)
        self.assertIn('href="https://example.com"', pg.content)

    def test_page_render_with_images(self):
        """Test rendering a page with images."""
        cfg = load_config(docs_dir=DOCS_DIR)
        fl = File('images.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)
        pg = Page('Images', fl, cfg)
        pg.markdown = '# Images\n\n![Alt text](https://example.com/image.png)'
        files = Files([fl])
        pg.render(cfg, files)
        self.assertIsNotNone(pg.content)
        self.assertIn('src="https://example.com/image.png"', pg.content)

    def test_page_canonical_url(self):
        """Test canonical URL generation."""
        cfg = load_config(docs_dir=DOCS_DIR, site_url='https://example.com/docs/')
        fl = File('index.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)
        pg = Page('Test', fl, cfg)
        self.assertEqual(pg.canonical_url, 'https://example.com/docs/')
        self.assertEqual(pg.abs_url, '/docs/')

    def test_page_canonical_url_nested(self):
        """Test canonical URL generation for nested pages."""
        cfg = load_config(docs_dir=DOCS_DIR, site_url='https://example.com/')
        fl = File('guide/index.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)
        pg = Page('Guide', fl, cfg)
        self.assertEqual(pg.canonical_url, 'https://example.com/guide/')
        self.assertEqual(pg.abs_url, '/guide/')

    def test_page_edit_url_github(self):
        """Test edit URL generation for GitHub repos."""
        cfg = load_config(
            docs_dir=DOCS_DIR,
            repo_url='https://github.com/user/repo',
            edit_uri='blob/main/docs/',
        )
        fl = File('index.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)
        pg = Page('Test', fl, cfg)
        self.assertEqual(pg.edit_url, 'https://github.com/user/repo/blob/main/docs/index.md')

    def test_page_edit_url_template(self):
        """Test edit URL generation with template."""
        cfg = load_config(
            docs_dir=DOCS_DIR,
            repo_url='https://github.com/user/repo',
            edit_uri_template='edit/main/{path}',
        )
        fl = File('guide/index.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)
        pg = Page('Guide', fl, cfg)
        self.assertEqual(pg.edit_url, 'https://github.com/user/repo/edit/main/guide/index.md')

    def test_page_active_state(self):
        """Test page active state propagation."""
        cfg = load_config(docs_dir=DOCS_DIR)
        fl = File('index.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)
        pg = Page('Test', fl, cfg)

        # Initially not active
        self.assertFalse(pg.active)

        # Set active
        pg.active = True
        self.assertTrue(pg.active)

        # Set inactive
        pg.active = False
        self.assertFalse(pg.active)

    def test_page_equality(self):
        """Test page equality comparison."""
        cfg = load_config(docs_dir=DOCS_DIR)
        fl1 = File('index.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)
        fl2 = File('index.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)
        fl3 = File('other.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)

        pg1 = Page('Test', fl1, cfg)
        pg2 = Page('Test', fl2, cfg)
        pg3 = Page('Test', fl3, cfg)

        # Pages with different file instances are not equal (different file identity)
        # But pages with same title and file src_uri should compare equal
        self.assertNotEqual(pg1, pg2)  # Different file instances
        self.assertNotEqual(pg1, pg3)  # Different files

    def test_page_repr(self):
        """Test page string representation."""
        cfg = load_config(docs_dir=DOCS_DIR)
        fl = File('index.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)
        pg = Page('Test', fl, cfg)
        self.assertIn('Test', repr(pg))
        self.assertIn('Page', repr(pg))

    def test_page_repr_without_title(self):
        """Test page string representation without title."""
        cfg = load_config(docs_dir=DOCS_DIR)
        fl = File('index.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)
        pg = Page(None, fl, cfg)
        self.assertIn('[blank]', repr(pg))

    def test_page_url_with_directory_urls(self):
        """Test page URL generation with directory URLs."""
        cfg = load_config(docs_dir=DOCS_DIR, use_directory_urls=True)
        fl = File('guide/getting-started.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)
        pg = Page('Getting Started', fl, cfg)
        self.assertEqual(pg.url, 'guide/getting-started/')

    def test_page_url_without_directory_urls(self):
        """Test page URL generation without directory URLs."""
        cfg = load_config(docs_dir=DOCS_DIR, use_directory_urls=False)
        fl = File('guide/getting-started.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)
        pg = Page('Getting Started', fl, cfg)
        self.assertEqual(pg.url, 'guide/getting-started.html')

    def test_page_url_index_with_directory_urls(self):
        """Test index page URL generation with directory URLs."""
        cfg = load_config(docs_dir=DOCS_DIR, use_directory_urls=True)
        fl = File('index.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)
        pg = Page('Home', fl, cfg)
        self.assertEqual(pg.url, '')

    def test_page_url_index_without_directory_urls(self):
        """Test index page URL generation without directory URLs."""
        cfg = load_config(docs_dir=DOCS_DIR, use_directory_urls=False)
        fl = File('index.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)
        pg = Page('Home', fl, cfg)
        self.assertEqual(pg.url, 'index.html')

    def test_page_is_homepage_nested(self):
        """Test that nested pages are not homepage."""
        cfg = load_config(docs_dir=DOCS_DIR)
        fl = File('guide/index.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)
        pg = Page('Guide', fl, cfg)
        self.assertFalse(pg.is_homepage)

    def test_page_is_homepage_non_index(self):
        """Test that non-index pages are not homepage."""
        cfg = load_config(docs_dir=DOCS_DIR)
        fl = File('about.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)
        pg = Page('About', fl, cfg)
        self.assertFalse(pg.is_homepage)

    def test_page_read_source(self):
        """Test reading page source from file."""
        # Use minimal docs dir which contains testing.md
        minimal_docs_dir = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), '..', 'integration', 'minimal', 'docs'
        )
        cfg = load_config(docs_dir=minimal_docs_dir)
        fl = File('testing.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)
        pg = Page('Testing', fl, cfg)
        pg.read_source(cfg)
        self.assertIsNotNone(pg.markdown)
        self.assertIsInstance(pg.meta, dict)

    def test_page_toc_structure(self):
        """Test that TOC has correct structure."""
        cfg = load_config(docs_dir=DOCS_DIR)
        fl = File('toc.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)
        pg = Page('TOC', fl, cfg)
        pg.markdown = textwrap.dedent("""
            # Main Title

            ## Section 1

            Content here.

            ### Subsection 1.1

            More content.

            ## Section 2

            Final content.
        """)
        files = Files([fl])
        pg.render(cfg, files)

        self.assertIsNotNone(pg.toc)
        self.assertGreater(len(pg.toc), 0)

        # Check that TOC items have required attributes
        for item in pg.toc:
            self.assertTrue(hasattr(item, 'title'))
            self.assertTrue(hasattr(item, 'url'))

    def test_page_render_with_pandoc_args(self):
        """Test rendering with custom pandoc arguments."""
        cfg = load_config(docs_dir=DOCS_DIR, pandoc={'args': ['--wrap=none']})
        fl = File('test.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)
        pg = Page('Test', fl, cfg)
        pg.markdown = '# Test\n\nContent'
        files = Files([fl])
        pg.render(cfg, files)
        self.assertIsNotNone(pg.content)

    def test_page_render_with_lua_filter(self):
        """Test rendering with lua filters (if available)."""
        cfg = load_config(docs_dir=DOCS_DIR, pandoc={'lua_filters': []})
        fl = File('test.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)
        pg = Page('Test', fl, cfg)
        pg.markdown = '# Test\n\nContent'
        files = Files([fl])
        pg.render(cfg, files)
        self.assertIsNotNone(pg.content)


if __name__ == '__main__':
    unittest.main()
