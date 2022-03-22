# Anki Image Scaler

An Anki plugin that scales images during editing. This plugin sets CSS
`max-height` property of all images in a note field to the desired value.

<p align="center">
  <img src="images/dune-scale.gif" height="350px"/>
</p>

## Background

I spend a lot of time solving Anki cards, and I believe that Anki notes should
look good. I solve most of my cards on my phone that, as any phone, has a small
screen, so when I create a new card, I usually scale down added images, so that
the card is pleasant to look at.

## Installation

### From AnkiWeb

You can install directly from
[AnkiWeb](https://ankiweb.net/shared/info/1312865748) using Anki's addon
management.

### From Source

1. Run `package`.
2. Import `imagescaler.ankiaddon` in Anki.

## Usage

Select a field with and image and press `CTRL+S`.

### Configuration

You can configure the plugin using Anki's configuration to do the following:

* Change the default height.
* Change the keyboard shortcut.
* Stop adding a scale button to the editor (the keyboard shortcut will still be active).

## For Developers

Use pipenv to set up the dev and prod environment.

### Testing

Run `testall` to run Mypy and unit tests.

### Publishing

The plugin is published and distributed on
[AnkiWeb](https://ankiweb.net/shared/info/1312865748).
