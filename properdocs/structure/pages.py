from __future__ import annotations

import enum
import logging
import posixpath
import warnings
from typing import TYPE_CHECKING, Any
from urllib.parse import unquote as urlunquote
from urllib.parse import urljoin, urlsplit, urlunsplit

from properdocs import utils
from properdocs.structure import StructureItem
from properdocs.structure.toc import get_toc
from properdocs.utils import get_build_date, get_markdown_title, meta, weak_property

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator, MutableMapping

    from properdocs.config.defaults import ProperDocsConfig
    from properdocs.structure.files import File, Files
    from properdocs.structure.toc import TableOfContents


log = logging.getLogger(__name__)


class Page(StructureItem):
    def __init__(self, title: str | None, file: File, config: ProperDocsConfig) -> None:
        file.page = self
        self.file = file
        if title is not None:
            self.title = title

        # Navigation attributes
        self.children = None
        self.previous_page = None
        self.next_page = None
        self.active = False

        self.update_date: str = get_build_date()

        self._set_canonical_url(config.get('site_url', None))
        self._set_edit_url(
            config.get('repo_url', None), config.get('edit_uri'), config.get('edit_uri_template')
        )

        # Placeholders to be filled in later in the build process.
        self.markdown = None
        self._title_from_render: str | None = None
        self.content = None
        self.toc = []  # type: ignore[assignment]
        self.meta = {}

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, self.__class__)
            and self.title == other.title
            and self.file == other.file
        )

    def __repr__(self):
        name = self.__class__.__name__
        title = f"{self.title!r}" if self.title is not None else '[blank]'
        url = self.abs_url or self.file.url
        return f"{name}(title={title}, url={url!r})"

    markdown: str | None
    """The original Markdown content from the file."""

    content: str | None
    """The rendered Markdown as HTML, this is the contents of the documentation.

    Populated after `.render()`."""

    toc: TableOfContents
    """An iterable object representing the Table of contents for a page. Each item in
    the `toc` is an [`AnchorLink`][properdocs.structure.toc.AnchorLink]."""

    meta: MutableMapping[str, Any]
    """A mapping of the metadata included at the top of the markdown page."""

    @property
    def url(self) -> str:
        """The URL of the page relative to the ProperDocs `site_dir`."""
        url = self.file.url
        if url in ('.', './'):
            return ''
        return url

    file: File
    """The documentation [`File`][properdocs.structure.files.File] that the page is being rendered from."""

    abs_url: str | None
    """The absolute URL of the page from the server root as determined by the value
    assigned to the [site_url][] configuration setting. The value includes any
    subdirectory included in the `site_url`, but not the domain. [base_url][] should
    not be used with this variable."""

    canonical_url: str | None
    """The full, canonical URL to the current page as determined by the value assigned
    to the [site_url][] configuration setting. The value includes the domain and any
    subdirectory included in the `site_url`. [base_url][] should not be used with this
    variable."""

    @property
    def active(self) -> bool:
        """When `True`, indicates that this page is the currently viewed page. Defaults to `False`."""
        return self.__active

    @active.setter
    def active(self, value: bool):
        """Set active status of page and ancestors."""
        self.__active = bool(value)
        if self.parent is not None:
            self.parent.active = bool(value)

    @property
    def is_index(self) -> bool:
        return self.file.name == 'index'

    edit_url: str | None
    """The full URL to the source page in the source repository. Typically used to
    provide a link to edit the source page. [base_url][] should not be used with this
    variable."""

    @property
    def is_homepage(self) -> bool:
        """Evaluates to `True` for the homepage of the site and `False` for all other pages."""
        return self.is_top_level and self.is_index and self.file.url in ('.', './', 'index.html')

    previous_page: Page | None
    """The [page][properdocs.structure.pages.Page] object for the previous page or `None`.
    The value will be `None` if the current page is the first item in the site navigation
    or if the current page is not included in the navigation at all."""

    next_page: Page | None
    """The [page][properdocs.structure.pages.Page] object for the next page or `None`.
    The value will be `None` if the current page is the last item in the site navigation
    or if the current page is not included in the navigation at all."""

    children: None = None
    """Pages do not contain children and the attribute is always `None`."""

    is_section: bool = False
    """Indicates that the navigation object is a "section" object. Always `False` for page objects."""

    is_page: bool = True
    """Indicates that the navigation object is a "page" object. Always `True` for page objects."""

    is_link: bool = False
    """Indicates that the navigation object is a "link" object. Always `False` for page objects."""

    def _set_canonical_url(self, base: str | None) -> None:
        if base:
            if not base.endswith('/'):
                base += '/'
            self.canonical_url = canonical_url = urljoin(base, self.url)
            self.abs_url = urlsplit(canonical_url).path
        else:
            self.canonical_url = None
            self.abs_url = None

    def _set_edit_url(
        self,
        repo_url: str | None,
        edit_uri: str | None = None,
        edit_uri_template: str | None = None,
    ) -> None:
        if not edit_uri_template and not edit_uri:
            self.edit_url = None
            return
        src_uri = self.file.edit_uri
        if src_uri is None:
            self.edit_url = None
            return

        if edit_uri_template:
            noext = posixpath.splitext(src_uri)[0]
            file_edit_uri = edit_uri_template.format(path=src_uri, path_noext=noext)
        else:
            assert edit_uri is not None and edit_uri.endswith('/')
            file_edit_uri = edit_uri + src_uri

        if repo_url:
            # Ensure urljoin behavior is correct
            if not file_edit_uri.startswith(('?', '#')) and not repo_url.endswith('/'):
                repo_url += '/'
        else:
            try:
                parsed_url = urlsplit(file_edit_uri)
                if not parsed_url.scheme or not parsed_url.netloc:
                    log.warning(
                        f"edit_uri: {file_edit_uri!r} is not a valid URL, it should include the http:// (scheme)"
                    )
            except ValueError as e:
                log.warning(f"edit_uri: {file_edit_uri!r} is not a valid URL: {e}")

        self.edit_url = urljoin(repo_url or '', file_edit_uri)

    def read_source(self, config: ProperDocsConfig) -> None:
        source = config.plugins.on_page_read_source(page=self, config=config)
        if source is None:
            try:
                source = self.file.content_string
            except OSError:
                log.error(f'File not found: {self.file.src_path}')
                raise
            except ValueError:
                log.error(f'Encoding error reading file: {self.file.src_path}')
                raise

        self.markdown, self.meta = meta.get_data(source)
        if config.get('pandoc_keep_frontmatter', False):
            self.markdown = source

    def _set_title(self) -> None:
        warnings.warn(
            "_set_title is no longer used in ProperDocs and will be removed soon.",
            DeprecationWarning,
        )

    @weak_property
    def title(self) -> str | None:  # type: ignore[override]
        """
        Returns the title for the current page.

        Before calling `read_source()`, this value is empty. It can also be updated by `render()`.

        Checks these in order and uses the first that returns a valid title:

        - value provided on init (passed in from config)
        - value of metadata 'title'
        - content of the first H1 in Markdown content
        - convert filename to title
        """
        if self.markdown is None:
            return None

        if 'title' in self.meta:
            return self.meta['title']

        if self._title_from_render:
            return self._title_from_render
        elif self.content is None:  # Preserve legacy behavior only for edge cases in plugins.
            title_from_md = get_markdown_title(self.markdown)
            if title_from_md is not None:
                return title_from_md

        if self.is_homepage:
            return 'Home'

        title = self.file.name.replace('-', ' ').replace('_', ' ')
        # Capitalize if the filename was all lowercase, otherwise leave it as-is.
        if title.lower() == title:
            title = title.capitalize()
        return title

    def render(self, config: ProperDocsConfig, files: Files) -> None:
        """Convert the Markdown source file to HTML as per the config."""
        if self.markdown is None:
            raise RuntimeError("`markdown` field hasn't been set (via `read_source`)")

        import pypandoc

        extra_args = list(config.get('pandoc_args', []))
        for lua_filter in config.get('pandoc_lua_filters', []):
            extra_args.append(f'--lua-filter={lua_filter}')

        # Add --quiet to suppress Pandoc warnings about unclosed tags
        if '--quiet' not in extra_args:
            extra_args.append('--quiet')

        try:
            html_output = pypandoc.convert_text(
                self.markdown,
                to=config.get('pandoc_to', 'html5'),
                format=config.get('pandoc_format', 'markdown'),
                extra_args=extra_args,
                filters=config.get('pandoc_filters', []),
            )
        except Exception as e:
            log.error(f"Error rendering {self.file.src_path} with Pandoc: {e}")
            raise

        parser = _PandocHTMLParser(self.file, files, config)
        self.content = parser.process(html_output)

        self.toc = get_toc(parser.build_toc_tokens())
        self._title_from_render = parser.title
        self.present_anchor_ids = parser.present_anchor_ids
        self.links_to_anchors = parser.links_to_anchors

    present_anchor_ids: set[str] | None = None
    """Anchor IDs that this page contains (can be linked to in this page)."""

    links_to_anchors: dict[File, dict[str, str]] | None = None
    """Links to anchors in other files that this page contains.

    The structure is: `{file_that_is_linked_to: {'anchor': 'original_link/to/some_file.md#anchor'}}`.
    Populated after `.render()`.
    """

    def validate_anchor_links(self, *, files: Files, log_level: int) -> None:
        if not self.links_to_anchors:
            return
        for to_file, links in self.links_to_anchors.items():
            for anchor, original_link in links.items():
                page = to_file.page
                if page is None:
                    continue
                if page.present_anchor_ids is None:  # Page was somehow not rendered.
                    continue
                if anchor in page.present_anchor_ids:
                    continue
                context = ""
                if to_file == self.file:
                    problem = "there is no such anchor on this page"
                    if anchor.startswith('fnref:'):
                        context = " This seems to be a footnote that is never referenced."
                else:
                    problem = f"the doc '{to_file.src_uri}' does not contain an anchor '#{anchor}'"
                log.log(
                    log_level,
                    f"Doc file '{self.file.src_uri}' contains a link '{original_link}', but {problem}.{context}",
                )


class _AbsoluteLinksValidationValue(enum.IntEnum):
    RELATIVE_TO_DOCS = -1


class _PandocHTMLParser:
    """Parses Pandoc-generated HTML to extract anchors, rewrite links, extract title and build TOC."""

    def __init__(self, file: File, files: Files, config: ProperDocsConfig):
        self.file = file
        self.files = files
        self.config = config

        self.present_anchor_ids: set[str] = set()
        self.links_to_anchors: dict[File, dict[str, str]] = {}

        self.title: str | None = None
        self.toc_tokens: list[dict[str, Any]] = []

    def process(self, html_output: str) -> str:
        import logging

        from bs4 import BeautifulSoup

        # Get the HTML parser from config, default to html.parser
        parser = self.config.get('html_parser', 'html.parser')

        # Suppress html5lib warnings about unclosed tags if using html5lib
        html5lib_logger = logging.getLogger("html5lib")
        old_level = html5lib_logger.level
        if parser == 'html5lib':
            html5lib_logger.setLevel(logging.ERROR)
        try:
            soup = BeautifulSoup(html_output, parser)
        finally:
            if parser == 'html5lib':
                html5lib_logger.setLevel(old_level)

        # 1. Extract anchors
        for tag in soup.find_all(id=True):
            self.present_anchor_ids.add(tag['id'])
        for a in soup.find_all('a', attrs={'name': True}):
            self.present_anchor_ids.add(a['name'])

        # 2. Extract Headings and build TOC
        for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            level = int(tag.name[1])
            anchor_id = tag.get('id', '')
            name = tag.get_text().strip()

            if self.title is None and level == 1:
                self.title = name

            self.toc_tokens.append({'level': level, 'id': anchor_id, 'name': name})

        # 3. Rewrite Links
        for a in soup.find_all('a', href=True):
            url = a['href']
            assert isinstance(url, str)
            new_url = self._path_to_url(url)
            if new_url != url:
                a['href'] = new_url

        for img in soup.find_all('img', src=True):
            url = img['src']
            assert isinstance(url, str)
            new_url = self._path_to_url(url)
            if new_url != url:
                img['src'] = new_url

        if soup.body:
            return soup.body.decode_contents()
        else:
            return str(soup)

    @classmethod
    def _target_uri(cls, src_path: str, dest_path: str) -> str:
        return posixpath.normpath(
            posixpath.join(posixpath.dirname(src_path), dest_path).lstrip('/')
        )

    @classmethod
    def _possible_target_uris(
        cls, file: File, path: str, use_directory_urls: bool, suggest_absolute: bool = False
    ) -> Iterator[str]:
        target_uri = cls._target_uri(file.src_uri, path)
        yield target_uri

        if posixpath.normpath(path) == '.':
            yield file.src_uri
            return
        tried = {target_uri}

        prefixes = [target_uri, cls._target_uri(file.url, path)]
        if prefixes[0] == prefixes[1]:
            prefixes.pop()

        suffixes: list[Callable[[str], str]] = []
        if use_directory_urls:
            suffixes.append(lambda p: p)
        if not posixpath.splitext(target_uri)[-1]:
            suffixes.append(lambda p: posixpath.join(p, 'index.md'))
            suffixes.append(lambda p: posixpath.join(p, 'README.md'))
        if (
            not target_uri.endswith('.')
            and not path.endswith('.md')
            and (use_directory_urls or not path.endswith('/'))
        ):
            suffixes.append(lambda p: p.removesuffix('.html') + '.md')

        for pref in prefixes:
            for suf in suffixes:
                guess = posixpath.normpath(suf(pref))
                if guess not in tried and not guess.startswith('../'):
                    yield guess
                    tried.add(guess)

    def _path_to_url(self, url: str) -> str:
        try:
            scheme, netloc, path, query, anchor = urlsplit(url)
        except ValueError:
            log.log(
                self.config.validation.links.unrecognized_links,
                f"Doc file '{self.file.src_uri}' contains an invalid link '{url}', "
                f"it was left as is.",
            )
            return url

        absolute_link = None
        warning_level, warning = 0, ''

        if scheme or netloc:
            return url
        elif url.startswith(('/', '\\')):
            absolute_link = self.config.validation.links.absolute_links
            if absolute_link is not _AbsoluteLinksValidationValue.RELATIVE_TO_DOCS:
                warning_level = absolute_link
                warning = f"Doc file '{self.file.src_uri}' contains an absolute link '{url}', it was left as is."
        elif not path:
            if anchor:
                self.links_to_anchors.setdefault(self.file, {}).setdefault(anchor, url)
            return url

        path = urlunquote(path)
        possible_target_uris = self._possible_target_uris(
            self.file, path, self.config.use_directory_urls
        )

        if warning:
            target_uri = url
            target_file = None
        else:
            target_uri = next(possible_target_uris)
            target_file = self.files.get_file_from_path(target_uri)

        if target_file is None and not warning:
            if not posixpath.splitext(path)[-1] and absolute_link is None:
                warning_level = self.config.validation.links.unrecognized_links
                warning = (
                    f"Doc file '{self.file.src_uri}' contains an unrecognized relative link '{url}', "
                    f"it was left as is."
                )
            else:
                target = f" '{target_uri}'" if target_uri != url.lstrip('/') else ""
                warning_level = self.config.validation.links.not_found
                warning = (
                    f"Doc file '{self.file.src_uri}' contains a link '{url}', "
                    f"but the target{target} is not found among documentation files."
                )

        if warning:
            if self.file.inclusion.is_excluded():
                warning_level = min(logging.INFO, warning_level)

            if warning_level > logging.DEBUG:
                suggest_url = ''
                for path in possible_target_uris:
                    if self.files.get_file_from_path(path) is not None:
                        if anchor and path == self.file.src_uri:
                            path = ''
                        elif absolute_link is _AbsoluteLinksValidationValue.RELATIVE_TO_DOCS:
                            path = '/' + path
                        else:
                            path = utils.get_relative_url(path, self.file.src_uri)
                        suggest_url = urlunsplit(('', '', path, query, anchor))
                        break
                else:
                    if '@' in url and '.' in url and '/' not in url:
                        suggest_url = f'mailto:{url}'
                if suggest_url:
                    warning += f" Did you mean '{suggest_url}'?"
            log.log(warning_level, warning)
            return url

        assert target_uri is not None
        assert target_file is not None

        if anchor:
            self.links_to_anchors.setdefault(target_file, {}).setdefault(anchor, url)

        if target_file.inclusion.is_excluded():
            if self.file.inclusion.is_excluded():
                warning_level = logging.DEBUG
            else:
                warning_level = min(logging.INFO, self.config.validation.links.not_found)
            warning = (
                f"Doc file '{self.file.src_uri}' contains a link to "
                f"'{target_uri}' which is excluded from the built site."
            )
            log.log(warning_level, warning)

        path = utils.get_relative_url(target_file.url, self.file.url)
        return urlunsplit(('', '', path, query, anchor))

    def build_toc_tokens(self) -> list[dict[str, Any]]:
        root = []
        stack = []
        for item in self.toc_tokens:
            node = {'level': item['level'], 'id': item['id'], 'name': item['name'], 'children': []}
            while stack and stack[-1]['level'] >= node['level']:
                stack.pop()
            if not stack:
                root.append(node)
            else:
                stack[-1]['children'].append(node)
            stack.append(node)
        return root
