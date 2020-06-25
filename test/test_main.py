#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from imagescaler import main
from typing import Optional


def stub_height_provider(default_height: int) -> main.HeightProvider:
    def height_provider(img: str) -> Optional[int]:
        return default_height

    return height_provider


class ScaleWithCssTestCase(unittest.TestCase):
    def test_scales_an_image(self):
        input = ('<div><img src="a.png"/></div>')
        expected_output = (
            '<div><img src="a.png" style="max-height:200px;"/></div>')
        self.assertEqual(
            main.scale_images_with_css(input, stub_height_provider(200)),
            expected_output)

    def test_scales_an_image_with_style(self):
        input = ('<div><img src="a.png" style="border:1px;"/></div>')
        expected_output = (
            '<div><img src="a.png" style="border:1px;max-height:200px;"/></div>'
        )
        self.assertEqual(
            main.scale_images_with_css(input, stub_height_provider(200)),
            expected_output)

    def test_rescales_an_image(self):
        input = ('<div><img src="a.png" style="max-height:300px;"/></div>')
        expected_output = (
            '<div><img src="a.png" style="max-height:200px;"/></div>')
        self.assertEqual(
            main.scale_images_with_css(input, stub_height_provider(200)),
            expected_output)

    def test_scales_through_cloze(self):
        input = '<div>{{c1::<img src="dune.jpg"/>}}</div>'
        expected_output = (
            '<div>{{c1::<img src="dune.jpg" style="max-height:200px;"/>}}' +
            '</div>')
        self.assertEqual(
            main.scale_images_with_css(input, stub_height_provider(200)),
            expected_output)

    def test_scales_multiple_images_differently(self):
        # 2 different sizes and also an image that is ignored.
        def height_generator(img: str) -> Optional[int]:
            if img == 'context.jpg':
                return 100
            elif img == 'img.jpg':
                return 200
            else:
                return None

        input = ('<div><img src="context.jpg"/><img src="ignore.jpg"/>' +
                 '<img src="img.jpg"/></div>')
        expected_output = (
            '<div><img src="context.jpg" style="max-height:100px;"/>' +
            '<img src="ignore.jpg"/>' +
            '<img src="img.jpg" style="max-height:200px;"/></div>')
        self.assertEqual(main.scale_images_with_css(input, height_generator),
                         expected_output)

    def test_scale_correctly_formats_html(self):
        input = '<div>&lt;img&gt;</div>'
        expected_output = '<div>&lt;img&gt;</div>'
        self.assertEqual(
            main.scale_images_with_css(input, stub_height_provider(200)),
            expected_output)
