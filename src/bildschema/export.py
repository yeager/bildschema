"""Export/print functionality for Bildschema schedules."""

import csv
import io
import json
from datetime import datetime

import gettext
_ = gettext.gettext

from bildschema import __version__

APP_LABEL = "Bildschema"
AUTHOR = "Daniel Nylander"

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib


def activities_to_csv(activities):
    """Export activities as CSV string."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([_("Activity"), _("Duration (min)"), _("Completed")])
    for act in activities:
        writer.writerow([
            act.get("name", ""),
            act.get("minutes", 0),
            _("Yes") if act.get("done") else _("No"),
        ])
    writer.writerow([])
    writer.writerow([f"{APP_LABEL} v{__version__} — {AUTHOR}"])
    return output.getvalue()


def activities_to_json(activities):
    """Export activities as JSON string."""
    data = {
        "app": APP_LABEL,
        "version": __version__,
        "author": AUTHOR,
        "exported": datetime.now().isoformat(),
        "activities": [
            {
                "name": a.get("name", ""),
                "minutes": a.get("minutes", 0),
                "done": a.get("done", False),
                "icon": a.get("icon", ""),
            }
            for a in activities
        ],
    }
    return json.dumps(data, indent=2, ensure_ascii=False)


def activities_to_pdf(activities, output_path):
    """Export schedule as A4 PDF using cairo."""
    try:
        import cairo
    except ImportError:
        try:
            import cairocffi as cairo
        except ImportError:
            return False

    width, height = 595, 842
    surface = cairo.PDFSurface(output_path, width, height)
    ctx = cairo.Context(surface)

    # Title
    ctx.set_font_size(24)
    ctx.move_to(40, 50)
    ctx.show_text(_("Daily Schedule"))

    ctx.set_font_size(12)
    ctx.set_source_rgb(0.5, 0.5, 0.5)
    ctx.move_to(40, 70)
    ctx.show_text(datetime.now().strftime("%Y-%m-%d"))
    ctx.set_source_rgb(0, 0, 0)

    y = 100
    row_h = 50

    for act in activities:
        if y + row_h > height - 40:
            surface.show_page()
            y = 40

        done = act.get("done", False)

        # Icon/emoji
        ctx.set_font_size(20)
        ctx.move_to(40, y + 30)
        ctx.show_text(act.get("icon", "📋"))

        # Name
        ctx.set_font_size(16)
        if done:
            ctx.set_source_rgb(0.6, 0.6, 0.6)
        else:
            ctx.set_source_rgb(0, 0, 0)
        ctx.move_to(80, y + 25)
        ctx.show_text(act.get("name", ""))

        # Duration
        ctx.set_font_size(11)
        ctx.set_source_rgb(0.5, 0.5, 0.5)
        ctx.move_to(80, y + 42)
        ctx.show_text(_("%d min") % act.get("minutes", 0))

        # Check mark
        if done:
            ctx.set_source_rgb(0.18, 0.76, 0.49)
            ctx.set_font_size(18)
            ctx.move_to(520, y + 28)
            ctx.show_text("✓")

        ctx.set_source_rgb(0.85, 0.85, 0.85)
        ctx.set_line_width(0.5)
        ctx.move_to(40, y + row_h - 2)
        ctx.line_to(width - 40, y + row_h - 2)
        ctx.stroke()
        ctx.set_source_rgb(0, 0, 0)

        y += row_h

    # Footer
    ctx.set_font_size(9)
    ctx.set_source_rgb(0.5, 0.5, 0.5)
    ctx.move_to(40, height - 20)
    ctx.show_text(f"{APP_LABEL} v{__version__} — {AUTHOR} — {datetime.now().strftime('%Y-%m-%d')}")

    surface.finish()
    return True


def show_export_dialog(window, activities, status_callback=None):
    """Show export dialog with CSV/JSON/PDF options."""
    dialog = Adw.AlertDialog.new(
        _("Export Schedule"),
        _("Choose export format:")
    )
    dialog.add_response("cancel", _("Cancel"))
    dialog.add_response("csv", _("CSV"))
    dialog.add_response("json", _("JSON"))
    dialog.add_response("pdf", _("PDF"))
    dialog.set_default_response("pdf")
    dialog.set_close_response("cancel")
    dialog.connect("response", _on_export_response, window, activities, status_callback)
    dialog.present(window)


def _on_export_response(dialog, response, window, activities, status_callback):
    if response == "cancel":
        return
    converters = {"csv": activities_to_csv, "json": activities_to_json}
    if response in converters:
        _save_text(window, activities, response, converters[response], status_callback)
    elif response == "pdf":
        _save_pdf(window, activities, status_callback)


def _save_text(window, activities, ext, converter, status_callback):
    fd = Gtk.FileDialog.new()
    fd.set_title(_("Save Export"))
    fd.set_initial_name(f"bildschema_{datetime.now().strftime('%Y%m%d')}.{ext}")
    fd.save(window, None, _on_text_done, activities, converter, ext, status_callback)


def _on_text_done(fd, result, activities, converter, ext, status_callback):
    try:
        gfile = fd.save_finish(result)
    except GLib.Error:
        return
    try:
        content = converter(activities)
        with open(gfile.get_path(), "w") as f:
            f.write(content)
        if status_callback:
            status_callback(_("Exported %s") % ext.upper())
    except Exception as e:
        if status_callback:
            status_callback(_("Export error: %s") % str(e))


def _save_pdf(window, activities, status_callback):
    fd = Gtk.FileDialog.new()
    fd.set_title(_("Save PDF"))
    fd.set_initial_name(f"bildschema_{datetime.now().strftime('%Y%m%d')}.pdf")
    fd.save(window, None, _on_pdf_done, activities, status_callback)


def _on_pdf_done(fd, result, activities, status_callback):
    try:
        gfile = fd.save_finish(result)
    except GLib.Error:
        return
    try:
        ok = activities_to_pdf(activities, gfile.get_path())
        if ok and status_callback:
            status_callback(_("PDF exported"))
        elif not ok and status_callback:
            status_callback(_("PDF export requires pycairo"))
    except Exception as e:
        if status_callback:
            status_callback(_("Export error: %s") % str(e))
