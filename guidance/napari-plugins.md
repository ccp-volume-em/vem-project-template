# napari plugins

From the guide: [Plugin development](https://ccp-volume-em.github.io/guide/plugins/)
and [Writing Tests For Plugins](https://ccp-volume-em.github.io/guide/plugin_testing/).

- Follow the official
  [napari plugin development guide](https://napari.org/stable/plugins/building_a_plugin/index.html).
  It includes a guided setup (with testing and GitHub Actions) and detailed
  implementation advice.
- Test each widget. In CI, pass a `napari.components.ViewerModel` as a mock
  viewer, add test images to it as layers, and run the widget's logic
  directly (without threads) rather than opening the GUI.
- Write installation tests checking that the plugin, napari and heavy
  dependencies (e.g. PyTorch) install and import together.
- If the plugin needs a GPU, mark GPU tests and skip them when no GPU is
  available. See [testing.md](testing.md).
- If the plugin will run in a container, see [containers.md](containers.md)
  for display (X11, Xpra) and start-up checks.

Keeping the analysis code in plain functions, separate from the widgets, lets
the same code run from the plugin, a CLI and notebooks; see
[large-data-and-workflows.md](large-data-and-workflows.md).
