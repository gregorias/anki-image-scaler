# 🛠️ Developer documentation

This is a documentation file for this plugin's developers.

## Dev Environment Setup

This project requires

- [Lefthook](https://github.com/evilmartians/lefthook)
- [Commitlint](https://github.com/conventional-changelog/commitlint)

1. Install the required Python version:

   ```shell
   pyenv install
   ```

1. Set up Pipenv:

    ```shell
    pipenv install --dev
    ```

1. Install Lefthook:

    ```shell
    lefthook install
    ```

## Testing

1. Run unit tests and MyPy with `testall`.
2. Test supported Anki versions (2.1.49 and latest) by packaging the
   plugin and importing the plugin into the lowest and the newest
   support Anki.

## Release & distribution

1. Create a release commit.
    1. Bump up the package version in `imagescaler/manifest.json`.
    2. Tag the release commit `git tag vx.y.z && git push origin vx.y.z`.
1. Use the `dev/bin/package` tool to create `imagescaler.ankiaddon`.
1. Create a GitHub release: `gh release create vx.y.z imagescaler.ankiaddon`.

1. [Share the package on Anki.](https://addon-docs.ankiweb.net/#/sharing)

## Publishing

The plugin is published and distributed on
[AnkiWeb](https://ankiweb.net/shared/info/1312865748).
