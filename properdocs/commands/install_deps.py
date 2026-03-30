import logging

import pypandoc.pandoc_download  # type: ignore[import-untyped]

log = logging.getLogger(__name__)


def install_deps() -> None:
    """Download and install the pandoc executable."""
    log.info("Downloading and installing pandoc...")
    pypandoc.pandoc_download.download_pandoc()
    log.info("Pandoc installation complete.")
