"""Image scaling functionality.

This module contains pure (without Anki) functions for scaling images in a
note. Anki is hard to test, so keeping non-Anki code separate helps."""
import copy
import re
import typing
from typing import Callable, Generator

import bs4
from bs4 import BeautifulSoup


class ImageSrc(typing.NamedTuple):
    src: str


PixelSize = int
HTML = str


def scale_an_image_with_css(img: bs4.element.Tag, size_property: str,
                            size: PixelSize) -> bs4.element.Tag:
    """
    Scales an image tag with the provided size.

    :param img bs4.element.Tag
    :param size_property str: The property we want to set (e.g., 'max-height').
    :param size PixelSize: The value of the size property.
    :rtype bs4.element.Tag
    """
    assert size >= 0
    img = copy.copy(img)
    if 'style' not in img.attrs:
        img.attrs['style'] = f'{size_property:s}:{size:d}px;'
        return img

    style = img.attrs['style']
    m = re.search(fr'{size_property}:[^;]*', style)

    if not m:
        if not style.endswith(';'):
            style += ';'
        style += f'{size_property:s}:{size:d}px;'
        img.attrs['style'] = style
        return img

    img.attrs['style'] = re.sub(fr'(?P<prefix>.*{size_property}:)[^;]*(.*)',
                                fr'\g<prefix>{size:d}px\2', style)
    return img


# I'm using a generator instead of a callback, because a generator is more
# generic. It allows tests to have a more natural control over this process.
def scale_images_with_css(
    size_property: str,
    html: HTML
) -> typing.Generator[ImageSrc, typing.Optional[PixelSize], HTML]:
    """
    Scales all images in the provided HTML.

    :param size_property str: The property we want to set (e.g., 'max-height').
    :param html HTML: The HTML with images to scale.
    :rtype typing.Generator[ImageSrc, typing.Optional[PixelSize], HTML]:
        A generator that asks for the desired size of each image.
    """
    bs = BeautifulSoup(html, features='html.parser')
    imgs = bs.findAll('img')
    for img in imgs:
        maybe_size = yield ImageSrc(src=img.attrs['src'])
        if not maybe_size:
            continue
        size = maybe_size
        assert size >= 0
        img.replace_with(scale_an_image_with_css(img, size_property, size))
    return str(bs)


Y = typing.TypeVar('Y')
S = typing.TypeVar('S')
Ret = typing.TypeVar('Ret')


def generator_to_callback(
        g: Generator[Y, S, Ret]) -> Callable[[Callable[[Y], S]], Ret]:
    """
    Converts a generator to a callback-based function.

    Useful for `scale_images_with_css`.

    :param g Generator[Y, S, Ret]
    :rtype Callable[[Callable[[Y], S]], Ret]
    """

    def handler(oracle: Callable[[Y], S]) -> Ret:
        try:
            hint = next(g)
            while True:
                send = oracle(hint)
                hint = g.send(send)
        except StopIteration as e:
            return e.value

    return handler
