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
* `add_editor_buttons` (default: true) – whether to show editor buttong
  (keyboard shortcuts will still be active).

To apply a new configuration, you need to restart Anki.

## For Developers

Use pipenv to set up the dev and prod environment.

### Dev Environment Setup

This project requires [Lefthook](https://github.com/evilmartians/lefthook) and
[Commitlint](https://github.com/conventional-changelog/commitlint).

1. Install the required Python version:

   ```shell
   pyenv install CHECK_PIPFILE
   ```

1. Set up Pipenv:

    ```shell
    pipenv install --dev
    ```

1. Install Lefthook:

    ```shell
    lefthook install
    ```

### Testing

1. Run unit tests and MyPy with `testall`.
2. Test supported Anki versions (2.1.49 and latest) by packaging the plugin and
   importing the plugin into the lowest and the newest support Anki.

### Release & distribution

1. Create a release commit.
    1. Bump up the package version in `imagescaler/manifest.json`.
    2. Tag the release commit `git tag vx.y.z && git push origin vx.y.z`.
2. Use the `dev/bin/package` tool to create `imagescaler.ankiaddon`.
3. [Share the package on Anki.](https://addon-docs.ankiweb.net/#/sharing)

### Publishing

The plugin is published and distributed on
[AnkiWeb](https://ankiweb.net/shared/info/1312865748).
