# Bildschema

Visual daily schedule with image support for children with autism and language disorders.

![Screenshot](screenshots/screenshot.png)

## Features

Activities displayed as cards with image + text, reorderable list, timer per activity, transition warnings. Day and week views.

## Requirements

- Python 3.10+
- GTK4 / libadwaita
- PyGObject

## Installation

```bash
# Install dependencies (Fedora/RHEL)
sudo dnf install python3-gobject gtk4 libadwaita

# Install dependencies (Debian/Ubuntu)
sudo apt install python3-gi gir1.2-gtk-4.0 gir1.2-adw-1

# Run from source
PYTHONPATH=src python3 -c "from bildschema.main import main; main()"
```

## License

GPL-3.0-or-later

## Author

Daniel Nylander

## Links

- [GitHub](https://github.com/yeager/bildschema)
- [Issues](https://github.com/yeager/bildschema/issues)
- [Translations](https://app.transifex.com/danielnylander/bildschema)
