from __future__ import annotations

import textwrap
import unittest

from properdocs.commands import build
from properdocs.structure.files import File, Files
from properdocs.structure.nav import get_navigation
from properdocs.structure.pages import Page
from properdocs.tests.base import PathAssertionMixin, load_config, tempdir
from properdocs.utils import meta


def build_page(title, path, config, md_src=''):
    """Helper which returns a Page object."""
    files = Files([File(path, config.docs_dir, config.site_dir, config.use_directory_urls)])
    page = Page(title, next(iter(files)), config)
    # Fake page.read_source()
    page.markdown, page.meta = meta.get_data(md_src)
    return page, files


class BuildTests(PathAssertionMixin, unittest.TestCase):
    def _get_env_with_null_translations(self, config):
        env = config.theme.get_env()
        env.add_extension('jinja2.ext.i18n')
        env.install_null_translations()
        return env

    # Test build.get_context

    def test_context_base_url_homepage(self):
        nav_cfg = [
            {'Home': 'index.md'},
        ]
        cfg = load_config(nav=nav_cfg, use_directory_urls=False)
        fs = [File('index.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)]
        files = Files(fs)
        nav = get_navigation(files, cfg)
        context = build.get_context(nav, files, cfg, nav.pages[0])
        self.assertEqual(context['base_url'], '.')

    def test_context_base_url_homepage_use_directory_urls(self):
        nav_cfg = [
            {'Home': 'index.md'},
        ]
        cfg = load_config(nav=nav_cfg)
        fs = [File('index.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)]
        files = Files(fs)
        nav = get_navigation(files, cfg)
        context = build.get_context(nav, files, cfg, nav.pages[0])
        self.assertEqual(context['base_url'], '.')

    def test_context_base_url_nested_page(self):
        nav_cfg = [
            {'Home': 'index.md'},
            {'Nested': 'foo/bar.md'},
        ]
        cfg = load_config(nav=nav_cfg, use_directory_urls=False)
        fs = [
            File('index.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls),
            File('foo/bar.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls),
        ]
        files = Files(fs)
        nav = get_navigation(files, cfg)
        context = build.get_context(nav, files, cfg, nav.pages[1])
        self.assertEqual(context['base_url'], '..')

    def test_context_base_url_nested_page_use_directory_urls(self):
        nav_cfg = [
            {'Home': 'index.md'},
            {'Nested': 'foo/bar.md'},
        ]
        cfg = load_config(nav=nav_cfg)
        fs = [
            File('index.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls),
            File('foo/bar.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls),
        ]
        files = Files(fs)
        nav = get_navigation(files, cfg)
        context = build.get_context(nav, files, cfg, nav.pages[1])
        self.assertEqual(context['base_url'], '../..')

    def test_context_base_url_relative_no_page(self):
        cfg = load_config(use_directory_urls=False, plugins=[])
        fs = [File('index.md', cfg.docs_dir, cfg.site_dir, cfg.use_directory_urls)]
        files = Files(fs)
        nav = get_navigation(files, cfg)
        context = build.get_context(nav, files, cfg, None)
        self.assertEqual(context['base_url'], '')

    # Test basic page rendering

    def test_page_render_basic(self):
        """Test that a page can be rendered with pypandoc."""
        cfg = load_config()
        page, files = build_page('Test', 'index.md', cfg, '# Hello World\n\nThis is a test.')
        page.render(cfg, files)
        self.assertIsNotNone(page.content)
        self.assertIn('Hello World', page.content)

    def test_page_render_with_code(self):
        """Test rendering a page with code blocks."""
        cfg = load_config()
        md_src = textwrap.dedent("""
            # Code Example

            ```python
            print("Hello, World!")
            ```
        """)
        page, files = build_page('Code', 'code.md', cfg, md_src)
        page.render(cfg, files)
        self.assertIsNotNone(page.content)
        self.assertIn('print', page.content)

    def test_page_render_with_links(self):
        """Test rendering a page with links."""
        cfg = load_config()
        md_src = '# Links\n\n[Example](https://example.com)'
        page, files = build_page('Links', 'links.md', cfg, md_src)
        page.render(cfg, files)
        self.assertIsNotNone(page.content)
        self.assertIn('href="https://example.com"', page.content)

    def test_page_render_with_images(self):
        """Test rendering a page with images."""
        cfg = load_config()
        # Use external URL to avoid validation warnings
        md_src = '# Images\n\n![Alt text](https://example.com/image.png)'
        page, files = build_page('Images', 'images.md', cfg, md_src)
        page.render(cfg, files)
        self.assertIsNotNone(page.content)
        self.assertIn('src="https://example.com/image.png"', page.content)

    # Test TOC generation

    def test_toc_generation(self):
        """Test that TOC is generated correctly."""
        cfg = load_config()
        md_src = textwrap.dedent("""
            # Main Title

            ## Section 1

            Content here.

            ## Section 2

            More content.
        """)
        page, files = build_page('TOC', 'toc.md', cfg, md_src)
        page.render(cfg, files)
        self.assertIsNotNone(page.toc)
        self.assertGreater(len(page.toc), 0)

    # Test build with config file

    @tempdir(
        {'mkpandocs.yml': 'site_name: Test\ntheme: mkdocs\nplugins: []', 'docs/index.md': '# Test'}
    )
    def test_build_simple_site(self, site_dir):
        """Test building a simple site."""
        import os

        old_cwd = os.getcwd()
        try:
            os.chdir(site_dir)
            from properdocs.config.base import load_config as base_load_config

            cfg = base_load_config()
            build.build(cfg)
            self.assertTrue(os.path.exists(os.path.join(site_dir, 'site', 'index.html')))
        finally:
            os.chdir(old_cwd)

    # Test error handling

    def test_build_missing_markdown(self):
        """Test that building a page without markdown raises an error."""
        cfg = load_config()
        page, files = build_page('Test', 'index.md', cfg)
        page.markdown = None
        with self.assertRaises(RuntimeError):
            page.render(cfg, files)


if __name__ == '__main__':
    unittest.main()
