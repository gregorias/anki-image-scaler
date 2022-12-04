"""TODO: describe this module
"""
import unittest

from imagescaler.imagescaler import generator_to_callback, scale_images_with_css, ImageSrc
from typing import Optional

class ScaleWithCssTestCase(unittest.TestCase):

    def test_scales_an_image(self):
        input = ('<div><img src="a.png"/></div>')
        expected_output = (
            '<div><img src="a.png" style="max-height:200px;"/></div>')

        g = scale_images_with_css("max-height", input)
        self.assertEqual(next(g), ImageSrc(src='a.png'))
        try:
            g.send(200)
        except StopIteration as s:
            self.assertEqual(s.value, expected_output)
        else:
            self.fail("Expected a return value.")

    def test_scales_on_max_width(self):
        input = ('<div><img src="a.png"/></div>')
        expected_output = (
            '<div><img src="a.png" style="max-width:200px;"/></div>')

        g = scale_images_with_css("max-width", input)
        self.assertEqual(next(g), ImageSrc(src='a.png'))
        try:
            g.send(200)
        except StopIteration as s:
            self.assertEqual(s.value, expected_output)
        else:
            self.fail("Expected a return value.")

    def test_scales_an_image_with_style(self):
        input = ('<div><img src="a.png" style="border:1px;"/></div>')
        expected_output = (
            '<div><img src="a.png" style="border:1px;max-height:200px;"/></div>'
        )

        g = scale_images_with_css("max-height", input)
        self.assertEqual(next(g), ImageSrc(src='a.png'))
        try:
            g.send(200)
        except StopIteration as s:
            self.assertEqual(s.value, expected_output)
        else:
            self.fail("Expected a return value.")

    def test_rescales_an_image(self):
        input = ('<div><img src="a.png" style="max-height:300px;"/></div>')
        expected_output = (
            '<div><img src="a.png" style="max-height:200px;"/></div>')

        g = scale_images_with_css("max-height", input)
        self.assertEqual(next(g), ImageSrc(src='a.png'))
        try:
            g.send(200)
        except StopIteration as s:
            self.assertEqual(s.value, expected_output)
        else:
            self.fail("Expected a return value.")

    def test_scales_through_cloze(self):
        input = '<div>{{c1::<img src="dune.jpg"/>}}</div>'
        expected_output = (
            '<div>{{c1::<img src="dune.jpg" style="max-height:200px;"/>}}' +
            '</div>')

        g = scale_images_with_css("max-height", input)
        self.assertEqual(next(g), ImageSrc(src='dune.jpg'))
        try:
            g.send(200)
        except StopIteration as s:
            self.assertEqual(s.value, expected_output)
        else:
            self.fail("Expected a return value.")

    def test_scales_multiple_images_differently(self):
        input = ('<div><img src="context.jpg"/><img src="ignore.jpg"/>' +
                 '<img src="img.jpg"/></div>')
        expected_output = (
            '<div><img src="context.jpg" style="max-height:100px;"/>' +
            '<img src="ignore.jpg"/>' +
            '<img src="img.jpg" style="max-height:200px;"/></div>')

        g = scale_images_with_css("max-height", input)
        self.assertEqual(next(g), ImageSrc(src='context.jpg'))
        self.assertEqual(g.send(100), ImageSrc(src='ignore.jpg'))
        self.assertEqual(g.send(None), ImageSrc(src='img.jpg'))
        try:
            g.send(200)
        except StopIteration as s:
            self.assertEqual(s.value, expected_output)
        else:
            self.fail("Expected a return value.")

    def test_scale_correctly_formats_html(self):
        input = '<div>&lt;img&gt;</div>'
        expected_output = '<div>&lt;img&gt;</div>'

        try:
            next(scale_images_with_css("max-height", input))
        except StopIteration as s:
            self.assertEqual(s.value, expected_output)
        else:
            self.fail("Expected a return value.")

class GeneratorToCallbackTestCase(unittest.TestCase):
    def test_converts_correctly(self):
        def generator():
            a = yield 1
            b = yield 2
            c = yield 3
            return [a, b, c]

        square = lambda i: i ** 2

        self.assertListEqual(generator_to_callback(generator())(square),
                             [1, 4, 9])


