# Anki Image Scaler

An Anki plugin that scales images during editing. This plugin sets CSS
`max-height` property (configurable) of all images in a note field to the
desired value.

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

### From GitHub Releases

You can fetch an addon package from [the GitHub Releases
tab](https://github.com/gregorias/anki-image-scaler/releases).

### From Source

1. Run `package`.
2. Import `imagescaler.ankiaddon` in Anki.

## Usage

Select a field with an image and press `CTRL+S` or `CTRL+ALT+B`.

### Configuration

You can configure the plugin using Anki's configuration with the following variables:

* `size-property` (default: "max-height") – the CSS property used by the
  plugin.
* `default-size` (default: 150) – the default pixel value suggested for
  `size-property`.
* `shortcut` — the keyboard shortcut for scaling individual images.
* `bulk_shortcut` — the keyboard shortcut for scaling all images in bulk.
* `add_editor_buttons` (default: true) – whether to show editor button
  (keyboard shortcuts will still be active).

To apply a new configuration, you need to restart Anki.
