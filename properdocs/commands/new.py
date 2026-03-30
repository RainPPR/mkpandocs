from __future__ import annotations

import logging
import os

config_text = 'site_name: My Docs\n'
index_text = """# Welcome to MkPandocs

For full documentation visit [mkpandocs.raincatsoft.com](https://mkpandocs.raincatsoft.com).

## Commands

* `mkpandocs new [dir-name]` - Create a new project.
* `mkpandocs serve` - Start the live-reloading docs server.
* `mkpandocs build` - Build the documentation site.
* `mkpandocs -h` - Print help message and exit.

## Project layout

    mkpandocs.yml # The configuration file.
    docs/
        index.md   # The documentation homepage.
        ...        # Other markdown pages, images and other files.
"""

log = logging.getLogger(__name__)


def new(output_dir: str) -> None:
    docs_dir = os.path.join(output_dir, 'docs')
    config_path = os.path.join(output_dir, 'mkpandocs.yml')
    index_path = os.path.join(docs_dir, 'index.md')

    if os.path.exists(config_path):
        log.info('Project already exists.')
        return

    if not os.path.exists(output_dir):
        log.info(f'Creating project directory: {output_dir}')
        os.mkdir(output_dir)

    log.info(f'Writing config file: {config_path}')
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(config_text)

    if os.path.exists(index_path):
        return

    log.info(f'Writing initial docs: {index_path}')
    if not os.path.exists(docs_dir):
        os.mkdir(docs_dir)
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_text)
