# -*- coding: utf-8 -*-
"""The implementation of the image scaler plugin."""
import os.path
import re
from typing import Any, Callable, List, Optional

import aqt  # type: ignore
from aqt import gui_hooks
from aqt.utils import showInfo, showWarning  # type: ignore

import bs4  # type: ignore
from bs4 import BeautifulSoup  # type: ignore
from PyQt5.QtWidgets import QInputDialog  # type: ignore

addon_path = os.path.dirname(__file__)
config = aqt.mw and aqt.mw.addonManager.getConfig(__name__)


def get_config(key: str, default):
    if config:
        return config.get(key, default)
    else:
        return default


HeightProvider = Callable[[str], Optional[int]]


def show_image_height_dialog(msg: str,
                             default_height: int,
                             parent=None) -> Optional[int]:
    parent = parent or (aqt.mw and aqt.mw.app.activeWindow()) or aqt.mw
    new_height, ok = QInputDialog.getInt(parent,
                                         'Enter image height',
                                         msg,
                                         value=default_height,
                                         min=0,
                                         max=10000)
    if ok:
        return new_height
    else:
        return None


def ask_for_new_height(image: str, parent=None) -> Optional[int]:
    return show_image_height_dialog(f'Provide a new height for {image} (px):',
                                    get_config('default-height', default=150),
                                    parent)


class BulkHeightProvider:

    def __init__(
        self,
        show_dialog: Callable[[str, int, Any],
                              Optional[int]] = show_image_height_dialog):
        self.height: None | bool | int = None
        self.show_dialog = show_dialog

    def __call__(self, image: str, parent=None) -> Optional[int]:
        if self.height == False:
            return None
        elif self.height:
            return self.height

        user_height = self.show_dialog(
            "Provide a new height for all images:",
            get_config('default-height', default=150), parent)
        if not user_height:
            self.height = False
            return user_height
        else:
            self.height = user_height
            return self.height


def scale_an_image_with_css(img: bs4.element.Tag, height: int) -> None:
    assert (height >= 0)
    if 'style' not in img.attrs:
        img.attrs['style'] = 'max-height:{height:d}px;'.format(height=height)
        return None

    style = img.attrs['style']
    m = re.search(r'max-height:[^;]*', style)

    if not m:
        if not style.endswith(';'):
            style += ';'
        style += 'max-height:{height:d}px;'.format(height=height)
        img.attrs['style'] = style
        return None

    img.attrs['style'] = re.sub(
        r'(?P<prefix>.*max-height:)[^;]*(.*)',
        r'\g<prefix>' + '{height:d}'.format(height=height) + r'px\2', style)


def scale_images_with_css(html: str, height_provider: HeightProvider) -> str:
    bs = BeautifulSoup(html, features='html.parser')
    imgs = bs.findAll('img')
    for img in imgs:
        maybe_height = height_provider(img.attrs['src'])
        if not maybe_height:
            continue
        height = maybe_height
        assert (height >= 0)
        scale_an_image_with_css(img, height)
    return str(bs)


def css_scale(
    editor: aqt.editor.Editor,
    height_provider: Callable[[str, aqt.editor.Editor],
                              Optional[int]]) -> None:
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
    # Provide the editor as the parent widget to ask_for_new_height. This way,
    # when ask_for_new_height's widget quits, focus goes back to the editor.
    new_field = scale_images_with_css(
        field, lambda img: height_provider(img, editor.widget))
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
    shortcut = get_config("shortcut", "ctrl+s")
    bulk_shortcut = get_config("bulk_shortcut", "ctrl+shift+s")
    add_buttons = get_config("add_editor_buttons", True)
    if add_buttons:
        icon_path = os.path.join(addon_path, "icons", "scale.png")
        css = editor.addButton(
            icon=icon_path,
            cmd="css_scale",
            func=lambda editor: css_scale(editor, ask_for_new_height),
            tip=f"Scale image using max-height ({shortcut}).",
            # Skip label, because we already provide an icon.
            keys=shortcut)
        buttons.append(css)
        css = editor.addButton(
            icon=icon_path,
            cmd="bulk_css_scale",
            func=lambda editor: css_scale(editor, BulkHeightProvider()),
            tip=f"Scale images in bulk using max-height ({bulk_shortcut}).",
            # Skip label, because we already provide an icon.
            keys=bulk_shortcut)
        buttons.append(css)
    else:
        aqt.qt.QShortcut(  # type: ignore
            aqt.qt.QKeySequence(shortcut),  # type: ignore
            editor.widget,
            activated=lambda: css_scale(editor, ask_for_new_height))
        aqt.qt.QShortcut(  # type: ignore
            aqt.qt.QKeySequence(bulk_shortcut),  # type: ignore
            editor.widget,
            activated=lambda: css_scale(editor, BulkHeightProvider()))


gui_hooks.editor_did_init_buttons.append(on_editor_buttons_init)
