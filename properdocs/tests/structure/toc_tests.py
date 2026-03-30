import unittest

from properdocs.structure.toc import get_toc
from properdocs.tests.base import dedent, get_pandoc_toc


class TableOfContentsTests(unittest.TestCase):
    def test_indented_toc(self):
        md = dedent(
            """
            # Heading 1
            ## Heading 2
            ### Heading 3
            """
        )
        toc = get_toc(get_markdown_toc(md))
        # Pandoc returns all headings, get_toc builds the tree
        toc_list = list(toc)
        self.assertGreater(len(toc_list), 0)
        self.assertEqual(toc_list[0].title, 'Heading 1')

    def test_flat_toc(self):
        md = dedent(
            """
            # Heading 1
            # Heading 2
            # Heading 3
            """
        )
        toc = get_toc(get_markdown_toc(md))
        toc_list = list(toc)
        self.assertEqual(len(toc_list), 3)
        self.assertEqual(toc_list[0].title, 'Heading 1')
        self.assertEqual(toc_list[1].title, 'Heading 2')
        self.assertEqual(toc_list[2].title, 'Heading 3')

    def test_flat_h2_toc(self):
        md = dedent(
            """
            ## Heading 1
            ## Heading 2
            ## Heading 3
            """
        )
        toc = get_toc(get_markdown_toc(md))
        toc_list = list(toc)
        self.assertEqual(len(toc_list), 3)

    def test_mixed_toc(self):
        md = dedent(
            """
            # Heading 1
            ## Heading 2
            # Heading 3
            ### Heading 4
            ### Heading 5
            """
        )
        toc = get_toc(get_markdown_toc(md))
        # Should have 2 top-level headings
        toc_list = list(toc)
        h1_items = [t for t in toc_list if t.level == 1]
        self.assertEqual(len(h1_items), 2)

    def test_level(self):
        md = dedent(
            """
            # Heading 1
            ## Heading 1.1
            ### Heading 1.1.1
            ### Heading 1.1.2
            ## Heading 1.2
            """
        )
        toc = get_toc(get_markdown_toc(md))

        def get_level_sequence(items):
            for item in items:
                yield item.level
                yield from get_level_sequence(item.children)

        self.assertEqual(tuple(get_level_sequence(toc)), (1, 2, 3, 3, 2))
