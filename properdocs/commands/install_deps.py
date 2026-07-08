import logging

import pypandoc  # type: ignore[import-untyped]
import pypandoc.pandoc_download  # type: ignore[import-untyped]
from tenacity import retry, stop_after_attempt, wait_chain, wait_fixed

log = logging.getLogger(__name__)


def before_retry_log(retry_state):
    log.info(f'Retrying pandoc download (attempt {retry_state.attempt_number})...')


@retry(
    stop=stop_after_attempt(10),
    wait=wait_chain(
        wait_fixed(2),
        wait_fixed(5),
        wait_fixed(10),
        wait_fixed(30),
        wait_fixed(60),
        wait_fixed(120),
        wait_fixed(180),
        wait_fixed(240),
        wait_fixed(300),
    ),
    before_sleep=before_retry_log,
)
def _download_pandoc_with_retry() -> None:
    """Download and install the pandoc executable with automatic retries."""
    log.info("Downloading and installing pandoc...")
    pypandoc.pandoc_download.download_pandoc()
    log.info("Pandoc installation complete.")


def install_deps() -> None:
    """Check if pandoc is installed; if not, download it."""
    try:
        # pypandoc.get_pandoc_version() will raise an OSError if pandoc is not found.
        version = pypandoc.get_pandoc_version()
    except OSError:
        log.info("Pandoc not found on the system. Proceeding with download.")
    else:
        # This executes only if no OSError was raised above
        log.info("Pandoc is already installed (version %s). Skipping download.", version)
        return

    # Call the decorated function to perform the download with retry automation
    _download_pandoc_with_retry()
