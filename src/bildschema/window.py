"""Main window for Bildschema."""
import gettext
import json
import os
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib, Gdk, GdkPixbuf

from . import arasaac
from .tts import speak

_ = gettext.gettext

# ARASAAC search terms for pictogram lookup (English terms for API)
SAMPLE_ACTIVITIES = [
    {"name": _("Wake up"), "icon": "🌅", "arasaac_term": "wake up", "minutes": 10},
    {"name": _("Breakfast"), "icon": "🥣", "arasaac_term": "breakfast", "minutes": 20},
    {"name": _("Get dressed"), "icon": "👕", "arasaac_term": "get dressed", "minutes": 15},
    {"name": _("School"), "icon": "🏫", "arasaac_term": "school", "minutes": 360},
    {"name": _("Lunch"), "icon": "🍽️", "arasaac_term": "lunch", "minutes": 30},
    {"name": _("Play"), "icon": "🎮", "arasaac_term": "play", "minutes": 60},
    {"name": _("Dinner"), "icon": "🍝", "arasaac_term": "dinner", "minutes": 30},
    {"name": _("Bath"), "icon": "🛁", "arasaac_term": "bath", "minutes": 20},
    {"name": _("Bedtime"), "icon": "🌙", "arasaac_term": "sleep", "minutes": 10},
]


class ActivityCard(Gtk.Box):
    def __init__(self, activity, index, on_done=None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        self.activity = activity
        self.index = index
        self.done = False
        self.add_css_class("card")
        self.set_margin_start(6)
        self.set_margin_end(6)
        self.set_margin_top(4)
        self.set_margin_bottom(4)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        hbox.set_margin_start(12)
        hbox.set_margin_end(12)
        hbox.set_margin_top(8)
        hbox.set_margin_bottom(8)

        # Try ARASAAC pictogram, fall back to emoji
        icon_widget = self._make_icon(activity)
        hbox.append(icon_widget)

        text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        text_box.set_hexpand(True)
        name_label = Gtk.Label(label=activity["name"], xalign=0)
        name_label.add_css_class("title-3")
        text_box.append(name_label)

        time_label = Gtk.Label(label=f"{activity.get('minutes', 0)} min", xalign=0)
        time_label.add_css_class("dim-label")
        text_box.append(time_label)
        hbox.append(text_box)

        speak_btn = Gtk.Button(icon_name="audio-speakers-symbolic")
        speak_btn.add_css_class("flat")
        speak_btn.add_css_class("circular")
        speak_btn.set_tooltip_text(_("Read aloud"))
        speak_btn.connect("clicked", lambda _: speak(activity["name"], "sv"))
        hbox.append(speak_btn)

        self.check = Gtk.CheckButton()
        self.check.connect("toggled", self._on_toggled)
        hbox.append(self.check)

        self.append(hbox)
        self._on_done = on_done

    @staticmethod
    def _make_icon(activity):
        """Create icon widget: ARASAAC pictogram if available, else emoji."""
        term = activity.get("arasaac_term")
        if term:
            try:
                provider = arasaac.get_provider()
                path = provider.get_pictogram(term, lang="en", resolution=96)
                if path:
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                        path, 48, 48, True)
                    image = Gtk.Image.new_from_pixbuf(pixbuf)
                    image.set_pixel_size(48)
                    return image
            except Exception:
                pass
        label = Gtk.Label(label=activity.get("icon", "📋"))
        label.add_css_class("title-1")
        return label

    def _on_toggled(self, btn):
        self.done = btn.get_active()
        if self.done:
            self.set_opacity(0.5)
        else:
            self.set_opacity(1.0)
        if self._on_done:
            self._on_done(self.index, self.done)


class BildschemaWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, default_width=500, default_height=700,
                         title=_("Visual Schedule"))
        self.activities = list(SAMPLE_ACTIVITIES)
        self._build_ui()
        self._start_clock()

    def _build_ui(self):
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(self.main_box)

        # Header
        header = Adw.HeaderBar()
        self.main_box.append(header)

        # Theme toggle
        theme_btn = Gtk.Button(icon_name="weather-clear-night-symbolic",
                               tooltip_text=_("Toggle dark/light theme"))
        theme_btn.connect("clicked", self._toggle_theme)
        header.pack_end(theme_btn)

        # Menu
        menu = Gio.Menu()
        menu.append(_("Export Schedule"), "app.export")
        menu.append(_("Preferences"), "app.preferences")
        menu.append(_("Keyboard Shortcuts"), "app.shortcuts")
        menu.append(_("About Visual Schedule"), "app.about")
        menu.append(_("Quit"), "app.quit")
        menu_btn = Gtk.MenuButton(icon_name="open-menu-symbolic",
                                  menu_model=menu)
        header.pack_end(menu_btn)

        # Add activity button
        add_btn = Gtk.Button(icon_name="list-add-symbolic",
                             tooltip_text=_("Add activity"))
        add_btn.connect("clicked", self._on_add_activity)
        header.pack_start(add_btn)

        # View switcher (day/week)
        view_box = Gtk.Box(spacing=0)
        view_box.add_css_class("linked")
        day_btn = Gtk.ToggleButton(label=_("Day"))
        day_btn.set_active(True)
        week_btn = Gtk.ToggleButton(label=_("Week"), group=day_btn)
        view_box.append(day_btn)
        view_box.append(week_btn)
        header.set_title_widget(view_box)

        # Scrolled activity list
        scrolled = Gtk.ScrolledWindow(vexpand=True)
        self.list_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self.list_box.set_margin_start(8)
        self.list_box.set_margin_end(8)
        self.list_box.set_margin_top(8)
        scrolled.set_child(self.list_box)
        self.main_box.append(scrolled)

        # Progress bar
        self.progress = Gtk.ProgressBar()
        self.progress.set_margin_start(12)
        self.progress.set_margin_end(12)
        self.progress.set_margin_top(4)
        self.progress.set_margin_bottom(4)
        self.main_box.append(self.progress)

        # Status bar
        self.status_label = Gtk.Label(label="", xalign=0)
        self.status_label.add_css_class("dim-label")
        self.status_label.set_margin_start(12)
        self.status_label.set_margin_bottom(4)
        self.main_box.append(self.status_label)

        self._populate()

    def _populate(self):
        child = self.list_box.get_first_child()
        while child:
            next_child = child.get_next_sibling()
            self.list_box.remove(child)
            child = next_child

        for i, act in enumerate(self.activities):
            card = ActivityCard(act, i, on_done=self._update_progress)
            self.list_box.append(card)
        self._update_progress(0, False)

    def _update_progress(self, idx, done):
        total = len(self.activities)
        if total == 0:
            return
        done_count = 0
        child = self.list_box.get_first_child()
        while child:
            if isinstance(child, ActivityCard) and child.done:
                done_count += 1
            child = child.get_next_sibling()
        frac = done_count / total
        self.progress.set_fraction(frac)
        self.progress.set_text(f"{done_count}/{total} " + _("completed"))
        self.progress.set_show_text(True)

    def _on_add_activity(self, btn):
        dialog = Adw.MessageDialog(
            transient_for=self,
            heading=_("Add Activity"),
            body=_("Enter activity name:"),
        )
        dialog.add_response("cancel", _("Cancel"))
        dialog.add_response("add", _("Add"))
        dialog.set_response_appearance("add", Adw.ResponseAppearance.SUGGESTED)

        entry = Gtk.Entry(placeholder_text=_("Activity name"))
        dialog.set_extra_child(entry)
        dialog.connect("response", self._on_add_response, entry)
        dialog.present()

    def _on_add_response(self, dialog, response, entry):
        if response == "add":
            name = entry.get_text().strip()
            if name:
                self.activities.append({"name": name, "icon": "📋", "minutes": 15})
                self._populate()

    def _toggle_theme(self, btn):
        mgr = Adw.StyleManager.get_default()
        if mgr.get_dark():
            mgr.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)
        else:
            mgr.set_color_scheme(Adw.ColorScheme.FORCE_DARK)

    def _start_clock(self):
        GLib.timeout_add_seconds(1, self._update_clock)
        self._update_clock()

    def _update_clock(self):
        now = GLib.DateTime.new_now_local()
        self.status_label.set_label(now.format("%Y-%m-%d %H:%M:%S"))
        return True
