# -*- coding: utf-8 -*-
"""The implementation of the image scaler plugin."""
import os.path
import re
from typing import List, Optional

import aqt
from aqt import gui_hooks
from aqt.utils import showInfo, showWarning

import bs4  # type: ignore
from bs4 import BeautifulSoup  # type: ignore
from PyQt5.QtWidgets import QInputDialog  # type: ignore

addon_path = os.path.dirname(__file__)
config = aqt.mw and aqt.mw.addonManager.getConfig(__name__)


def get_config(key: str, default):
    return (config and config.get(key, default)) or default


def ask_for_new_height() -> Optional[int]:
    parent = (aqt.mw and aqt.mw.app.activeWindow()) or aqt.mw
    new_height, ok = QInputDialog.getInt(
        parent,
        'Enter image height',
        'Provide a new height for the image (px):',
        value=get_config('default-height', default=150),
        min=0,
        max=10000)
    return ok and new_height


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


def scale_images_with_css(html: str, height: int) -> str:
    assert (height >= 0)
    bs = BeautifulSoup(html, features='html.parser')
    imgs = bs.findAll('img')
    for img in imgs:
        scale_an_image_with_css(img, height)
    return str(bs)


def css_scale(editor) -> None:
    if editor.currentField is None:
        showWarning(
            "You've run the image scaler without selecting a field.\n" +
            "Please select a note field before running the image scaler.")
        return None

    new_height = ask_for_new_height()
    if not new_height:
        return None

    field = editor.note.fields[editor.currentField]
    new_field = scale_images_with_css(field, new_height)
    editor.note.fields[editor.currentField] = new_field
    editor.note.flush()
    editor.mw.reset()


def on_editor_buttons_init(buttons: List, editor) -> None:
    shortcut = get_config("shortcut", "ctrl+s")
    icon_path = os.path.join(addon_path, "icons", "scale.png")
    css = editor.addButton(
        icon=icon_path,
        cmd="css_scale",
        func=css_scale,
        tip="Scale image using max-height ({}).".format(shortcut),
        # Skip label, because we already provide an icon.
        keys=shortcut)
    buttons.append(css)


gui_hooks.editor_did_init_buttons.append(on_editor_buttons_init)
