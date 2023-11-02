"""The implementation of the image scaler plugin."""
from functools import partial
import os.path
import re
from typing import Any, Callable, List, Optional, Union

import aqt
from aqt import gui_hooks
from aqt.utils import showInfo, showWarning

import bs4
from bs4 import BeautifulSoup
from aqt.qt import QInputDialog, QWidget

from . import imagescaler

addon_path = os.path.dirname(__file__)
config = aqt.mw and aqt.mw.addonManager.getConfig(__name__)


def get_config(key: str, default):
    if config:
        return config.get(key, default)
    else:
        return default


def show_image_size_dialog(msg: str,
                           size_property: str,
                           default_size: int,
                           parent=None) -> Optional[int]:
    parent = parent or (aqt.mw and aqt.mw.app.activeWindow()) or aqt.mw
    new_size, ok = QInputDialog.getInt(parent,
                                       f'Enter image {size_property}',
                                       msg,
                                       value=default_size,
                                       min=0,
                                       max=10000)
    if ok:
        return new_size
    else:
        return None


def ask_for_new_size(size_property: str,
                     default_size: imagescaler.PixelSize,
                     image: str,
                     parent=None) -> Optional[int]:
    return show_image_size_dialog(
        f'Provide a new {size_property} for {image} (px):', size_property,
        default_size, parent)


class BulkSizeProvider:

    def __init__(
        self,
        size_property: str,
        default_size: int,
        show_dialog: Callable[[str, str, int, Any],
                              Optional[int]] = show_image_size_dialog):
        self.size_property = size_property
        self.default_size = default_size
        self.size: Optional[Union[bool, int]] = None
        self.show_dialog = show_dialog

    def __call__(self, image: str, parent=None) -> Optional[int]:
        if self.size == False:
            return None
        elif self.size:
            return self.size

        user_size = self.show_dialog(
            f"Provide a new {self.size_property} for all images:",
            self.size_property, self.default_size, parent)
        if not user_size:
            self.size = False
            return user_size
        else:
            self.size = user_size
            return self.size


def css_scale(editor: aqt.editor.Editor, size_property: str,
              size_provider: Callable[[str, QWidget], Optional[int]]) -> None:
    # Save the currentField into a variable. Anki may turn editor.currentField
    # to None while running this function, because we show a dialog.
    currentField = editor.currentField
    currentNote = editor.note
    if currentField is None:
        showWarning(
            "You've run the image scaler without selecting a field.\n" +
            "Please select a note field before running the image scaler.")
        return None
    if currentNote is None:
        showWarning("You've run the image scaler without selecting a note.\n" +
                    "Please select a note before running the image scaler.")
        return None

    field = currentNote.fields[currentField]
    # Provide the editor as the parent widget to ask_for_new_size. This way,
    # when ask_for_new_size's widget quits, focus goes back to the editor.
    new_field = imagescaler.generator_to_callback(
        imagescaler.scale_images_with_css(
            size_property,
            field))(lambda imgSrc: size_provider(imgSrc.src, editor.widget))
    if new_field == field:
        # Don't bother refreshing the editor. It is disturbing, e.g., the field
        # loses focus, so we should avoid it.
        return
    currentNote.fields[currentField] = new_field
    # That's how aqt.editor.onHtmlEdit saves cards.
    # It's better than `editor.mw.reset()`, because the latter loses focus.
    # Calls like editor.mw.reset() or editor.loadNote() are necessary to save
    # HTML changes.
    if not editor.addMode:
        currentNote.flush()
    editor.loadNoteKeepingFocus()


def on_editor_buttons_init(buttons: List, editor: aqt.editor.Editor) -> None:
    size_property = get_config("size-property", "max-height")
    default_size = get_config('default-size', default=150)
    shortcut = get_config("shortcut", "ctrl+s")
    # Choosing the default as ctrl+alt+b, because:
    # * ctrl+shift+s is already taken by Anki.
    #   (https://anki.tenderapp.com/discussions/beta-testing/152-2034-beta-2-21-mar)
    # * ctrl+alt+s, ctrl+b are also taken by Anki.
    # * ctrl+shift+alt+s is taken by another plugin for centering text.
    # * b stands for bulk.
    bulk_shortcut = get_config("bulk_shortcut", "ctrl+alt+b")
    add_buttons = get_config("add_editor_buttons", True)
    if add_buttons:
        icon_path = os.path.join(addon_path, "icons", "scale.png")
        css = editor.addButton(
            icon=icon_path,
            cmd="css_scale",
            func=lambda editor: css_scale(
                editor, size_property,
                partial(ask_for_new_size, size_property, default_size)),
            tip=f"Scale image using {size_property} ({shortcut}).",
            # Skip label, because we already provide an icon.
            keys=shortcut)
        buttons.append(css)
        css = editor.addButton(
            icon=icon_path,
            cmd="bulk_css_scale",
            func=lambda editor: css_scale(
                editor, size_property,
                BulkSizeProvider(size_property, default_size)),
            tip=
            f"Scale images in bulk using {size_property} ({bulk_shortcut}).",
            # Skip label, because we already provide an icon.
            keys=bulk_shortcut)
        buttons.append(css)
    else:
        aqt.qt.QShortcut(  # type: ignore
            aqt.qt.QKeySequence(shortcut),  # type: ignore
            editor.widget,
            activated=lambda: css_scale(
                editor, size_property,
                partial(ask_for_new_size, size_property, default_size)))
        aqt.qt.QShortcut(  # type: ignore
            aqt.qt.QKeySequence(bulk_shortcut),  # type: ignore
            editor.widget,
            activated=lambda: css_scale(
                editor, size_property,
                BulkSizeProvider(size_property, default_size)))


gui_hooks.editor_did_init_buttons.append(on_editor_buttons_init)
