#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from imagescaler import main


class ScaleWithCssTestCase(unittest.TestCase):
    def test_scales_an_image(self):
        input = ('<div><img src="a.png"/></div>')
        expected_output = (
            '<div><img src="a.png" style="max-height:200px;"/></div>')
        self.assertEqual(main.scale_images_with_css(input, height=200),
                         expected_output)

    def test_scales_an_image_with_style(self):
        input = ('<div><img src="a.png" style="border:1px;"/></div>')
        expected_output = (
            '<div><img src="a.png" style="border:1px;max-height:200px;"/></div>'
        )
        self.assertEqual(main.scale_images_with_css(input, height=200),
                         expected_output)

    def test_rescales_an_image(self):
        input = ('<div><img src="a.png" style="max-height:300px;"/></div>')
        expected_output = (
            '<div><img src="a.png" style="max-height:200px;"/></div>')
        self.assertEqual(main.scale_images_with_css(input, height=200),
                         expected_output)

    def test_scales_through_cloze(self):
        input = '<div>{{c1::<img src="dune.jpg"/>}}</div>'
        expected_output = (
            '<div>{{c1::<img src="dune.jpg" style="max-height:200px;"/>}}' +
            '</div>')
        self.assertEqual(main.scale_images_with_css(input, height=200),
                         expected_output)
