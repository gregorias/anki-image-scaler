# Anki Image Scaler

An Anki plugin that scales images during editing. This plugin sets CSS
`max-height` property of all images in a note field to the desired value.

<p align="center">
  <img src="images/dune-scale.gif" height="350px"/>
</p>

## Background

I like to make sure my Anki notes look good. Having a card that is small enough
to display on a phone screen is a desirable property. That requires resizing
images, so that they are small.

## Installation

1. Run `package`.
2. Import `imagescaler.ankiaddon` in Anki.

## For Developers

Use pipenv to set up the dev and prod environment.

### Testing

Run `testall` to run Mypy and unit tests.
