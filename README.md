# Bildschema

Visual daily schedule with image support for children with autism and language disorders.

> **Målgrupp / Target audience:** Barn och vuxna med autism, språkstörning (DLD),
> intellektuell funktionsnedsättning och andra kognitiva funktionsnedsättningar som
> behöver visuellt stöd för att förstå och följa dagliga rutiner. Även användbart i
> förskola, skola och LSS-verksamhet.
>
> **For:** Children and adults with autism spectrum disorder (ASD), developmental
> language disorder (DLD), intellectual disabilities, and other cognitive disabilities
> who benefit from visual supports for daily routines. Also useful in preschools,
> schools, and disability services.

![Screenshot](screenshots/screenshot.png)

## Features

- Activities displayed as cards with image + text
- **ARASAAC pictogram support** — automatic download of free pictograms from
  [ARASAAC](https://arasaac.org) (CC BY-NC-SA, Government of Aragon / Sergio Palao)
- Emoji fallback when offline or pictograms unavailable
- Reorderable list, timer per activity, transition warnings
- Day and week views
- Dark/light theme toggle

## Free Image Resources

This app supports pictograms from these free/open sources:

| Resource | License | URL |
|----------|---------|-----|
| **ARASAAC** | CC BY-NC-SA 4.0 | https://arasaac.org |
| **OpenMoji** | CC BY-SA 4.0 | https://openmoji.org |
| **Mulberry Symbols** | CC BY-SA 2.0 UK | https://mulberrysymbols.org |
| **Sclera** | CC BY-NC 2.0 BE | https://sclera.be |

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

## ARASAAC Attribution

Pictographic symbols © Government of Aragon, created by Sergio Palao for
[ARASAAC](https://arasaac.org), distributed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).

## License

GPL-3.0-or-later

## Author

Daniel Nylander

## Links

- [GitHub](https://github.com/yeager/bildschema)
- [Issues](https://github.com/yeager/bildschema/issues)
- [Translations](https://app.transifex.com/danielnylander/bildschema)
