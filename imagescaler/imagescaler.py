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


def scale_an_image_with_css(img: bs4.element.Tag,
                            height: int) -> bs4.element.Tag:
    """
    Scales an image tag with the provided max-height value.

    :param img bs4.element.Tag
    :param height int
    :rtype bs4.element.Tag
    """
    assert height >= 0
    img = copy.copy(img)
    if 'style' not in img.attrs:
        img.attrs['style'] = 'max-height:{height:d}px;'.format(height=height)
        return img

    style = img.attrs['style']
    m = re.search(r'max-height:[^;]*', style)

    if not m:
        if not style.endswith(';'):
            style += ';'
        style += 'max-height:{height:d}px;'.format(height=height)
        img.attrs['style'] = style
        return img

    img.attrs['style'] = re.sub(
        r'(?P<prefix>.*max-height:)[^;]*(.*)',
        r'\g<prefix>' + '{height:d}'.format(height=height) + r'px\2', style)
    return img


# I'm using a generator instead of a callback, because a generator is more
# generic. It allows tests to have a more natural control over this process.
def scale_images_with_css(
    html: HTML
) -> typing.Generator[ImageSrc, typing.Optional[PixelSize], HTML]:
    """
    Scales all images in the provided HTML.

    :param html HTML: The HTML with images to scale.
    :rtype typing.Generator[ImageSrc, typing.Optional[PixelSize], HTML]:
        A generator that asks for the desired size of each image.
    """
    bs = BeautifulSoup(html, features='html.parser')
    imgs = bs.findAll('img')
    for img in imgs:
        maybe_height = yield ImageSrc(src=img.attrs['src'])
        if not maybe_height:
            continue
        height = maybe_height
        assert height >= 0
        img.replace_with(scale_an_image_with_css(img, height))
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
