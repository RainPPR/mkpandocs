# MkPandocs

[![PyPI Version][pypi-v-image]][pypi-v-link]
[![Build Status][GHAction-image]][GHAction-link]

MkPandocs is a static site generator intended for project documentation. Source files are written in Markdown and converted to static HTML during the build process.

Project configuration is defined in a YAML configuration file (`mkpandocs.yml`). This file specifies the documentation structure, theme configuration, and optional plugin settings.

MkPandocs supports extension through plugins, themes and Markdown extensions.

For usage instructions and examples, see the Documentation.

---

## Features

Current functionality includes:

- Conversion of Markdown source files into static HTML pages
- YAML-based configuration
- Plugin system for extending functionality
- Support for Markdown extensions
- Support for third-party themes
- Static output suitable for deployment on standard web servers

Additional functionality is available through plugins.

---

## Support

If you encounter problems while using MkPandocs, the following resources are available:

-   For questions and high-level discussions, use **[Discussions]** on GitHub.
    - For small questions, a good alternative is the **[Discord server]**.
-   To report a bug or make a feature request, open an **[Issue]** on GitHub.

Support is generally limited to **core MkPandocs functionality**. Issues related to third-party themes, plugins or extensions should normally be reported to the maintainers of those projects.

Questions about such components may still be discussed in chat.

---

## Links

- [Official Documentation][mkpandocs]
- [Latest Release Notes][release-notes]
- [Catalog of third-party plugins, themes and recipes][catalog]

---

## Contributing

Contributions are welcome.

For development setup, coding guidelines and contribution workflow, see the **[Contributing Guide]**.

---

## Code of Conduct

All participants in the MkPandocs project are expected to follow the **[PSF Code of Conduct]**.

---

## License

MkPandocs is distributed under the [**BSD-2-Clause license**](LICENSE).

<!-- Badges -->
[pypi-v-image]: https://img.shields.io/pypi/v/mkpandocs.svg
[pypi-v-link]: https://pypi.org/project/mkpandocs/
[GHAction-image]: https://github.com/RainPPR/mkpandocs/actions/workflows/ci.yml/badge.svg
[GHAction-link]: https://github.com/RainPPR/mkpandocs/actions/workflows/ci.yml

<!-- Links -->
[mkpandocs]: https://mkpandocs.raincatsoft.com
[Issue]: https://github.com/RainPPR/mkpandocs/issues
[Discussions]: https://github.com/RainPPR/mkpandocs/discussions
[Discord server]: https://discord.gg/CwYAgEPHZd
[release-notes]: https://mkpandocs.raincatsoft.com/about/release-notes/
[Contributing Guide]: https://mkpandocs.raincatsoft.com/about/contributing/
[PSF Code of Conduct]: https://www.python.org/psf/conduct/
[catalog]: https://github.com/properdocs/catalog
