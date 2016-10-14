## Outline for Sublime Text 3

### Overview

Inspired by [FileBrowser](https://github.com/aziz/SublimeFileBrowser), this package shows the outline/structure of your code/document in a sidebar-style tab.

![Screenshot](screenshot.png?raw=true "Screenshot")

### Installation

#### Install via Package Control

This package is available on Package Control. Search for `Outline`.

#### Manual installation

1. Clone or download this repository to your hard drive using the green `Clone or download` button
2. Rename the cloned or extracted folder to `Outline`. Make sure `outline.py` is at the root of the `Outline` folder.
3. Move the `Outline` folder to your Sublime Text's `Packages` folder. To find the `Packages` folder, click menu `Preferences` > `Browse Packages`.
4. Restart Sublime Text, and press `Ctrl + Shift + P` to select your preferred layout (`Browse Mode`)

### Default layout

The outline tab can be set as a sidebar on the left or right. Press `Ctrl + Shift + P` and select either `Browse Mode: Outline (Left)` or `Browse Mode: Outline (Right)` to set your preferred layout.

If you also use [FileBrowser](https://github.com/aziz/SublimeFileBrowser), you can use both in three different layouts:

* `FileBrowser` left, `Outline` right
* `FileBrowser` top left, `Outline` bottom left
* `FileBrowser` top right, `Outline` bottom right

To use `FileBrowser` and `Outline` together, please close the `FileBrowser` sidebar first and then use the correponding `Browse Mode` command to set the layout, otherwise the `Outline` view may not work as intended.

### Outline content and indentation

Outline is updated when you save a file or switch between files.

Content and indentation in the `Outline` tab is controlled by the `Symbol List.tmPreferences` file (file name may differ) corresponding to the syntax of your file.

### Known issue

* This package may not work if you use a multi-column/row layout.

### License

This plugin is licensed under the MIT license.
