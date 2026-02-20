# Bildschema

[![Version](https://img.shields.io/badge/version-0.2.0-blue)](https://github.com/yeager/bildschema/releases)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPL%203.0-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Transifex](https://img.shields.io/badge/Transifex-Translate-green.svg)](https://www.transifex.com/danielnylander/bildschema/)

Visual daily schedule with image support for children with autism and language disorders — GTK4/Adwaita.

> **For:** Children and adults with autism, developmental language disorder (DLD), ADHD, or intellectual disabilities. Visual daily planning with drag-and-drop image support.

![Screenshot](screenshots/main.png)

## Features

- **Daily schedule** — drag-and-drop visual planning
- **Image support** — custom images or ARASAAC pictograms
- **ARASAAC integration** — 13,000+ free pictograms
- **Categories** — morning, school, afternoon, evening
- **Print-friendly** — export schedules
- **Dark/light theme** toggle

## Installation

### Debian/Ubuntu

```bash
echo "deb [signed-by=/usr/share/keyrings/yeager-keyring.gpg] https://yeager.github.io/debian-repo stable main" | sudo tee /etc/apt/sources.list.d/yeager.list
curl -fsSL https://yeager.github.io/debian-repo/yeager-keyring.gpg | sudo tee /usr/share/keyrings/yeager-keyring.gpg > /dev/null
sudo apt update && sudo apt install bildschema
```

### Fedora/openSUSE

```bash
sudo dnf config-manager --add-repo https://yeager.github.io/rpm-repo/yeager.repo
sudo dnf install bildschema
```

### From source

```bash
git clone https://github.com/yeager/bildschema.git
cd bildschema && pip install -e .
bildschema
```

## ARASAAC Attribution

Pictographic symbols © Gobierno de Aragón, created by Sergio Palao for [ARASAAC](https://arasaac.org), distributed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).

## Translation

Help translate on [Transifex](https://www.transifex.com/danielnylander/bildschema/).

## License

GPL-3.0-or-later — see [LICENSE](LICENSE) for details.

## Author

**Daniel Nylander** — [danielnylander.se](https://danielnylander.se)
