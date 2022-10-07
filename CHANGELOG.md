# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.8.0] 2022-10-07

### Added

* Added `RobotObject`.
* Added `datastore` to `TreeForm`.
* Added `TabsForm`.
* Added `BRepObject`.
* Added `zoom_extents` to `Camera`.
* Added `expanded` option for `TreeForm` data entries.
* Added `striped_rows` option for `TreeForm`.
* Added `option` to display drop down list for `TreeForm` item editing.
* Added `on_object_selected` event listener.
* Added `use_vertex_color` option to `MeshObject`.

### Changed

* Give access to `self` in `TreeForm` click events.
* Allow `TreeForm` columns to be editable.
* Auto adjust first column width in `TreeForm`.
* Allow set colums individually in `TabsForm`.
* Fix `TabsForm` top margin display issue on macos.
* Fixed a `Ghostmode` bug.
* Allow `TabsFrom` to update.

### Removed


## [0.7.0] 2022-08-22

### Added

### Changed

* Moved `pointcolor`, `linecolor`, `facecolor` to `Object` from `BufferObject`.
* Exposing `pointcolor`, `linecolor`, `facecolor` at `App.add` for pylance linting.
* `pointcolor`, `linecolor`, `facecolor` now accept both single value or dictionary of values.

### Removed

* `pointcolors`, `linecolors`, `facecolors` are removed, use `pointcolor`, `linecolor`, `facecolor` instead.
* `treeform` is now more customizable.
* Removed placeholder menu items.

## [0.6.0] 2022-07-21

### Added

* Added dedicated Scene objects form.
* Added dedicated object property form.
* Added custom tree form.
* Added option to run multi-threading function.
* Added sidedock options.
* Added option to change App title.
* Added matplotlib integration.

### Changed

### Removed


## [0.5.0] 2022-03-22

### Added

* Added (optional) Ryven flow integration.
* Added Vector object.
* Separate shaders for background, model, and overlay objects.
* Collection object for large numbers of individual objects.

### Changed

* Changed blending of opacity to be based on camera distance.
* Updated workflow to latest.
* Reconstructed Camera class.
* Switch build workflow to run with conda.

### Removed
